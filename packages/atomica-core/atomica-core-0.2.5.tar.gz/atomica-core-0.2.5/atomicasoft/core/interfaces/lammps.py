"""
Lammps jobs + MD

Very limited functionality with LAMMPS potentials
"""

from ..jobs._basic import *

import re, json, numpy as np, warnings, hashlib, pathlib, io

from .. import ptable
from ..thermodynamics import Concentration, Energy, Pressure, Term, TermContainer
from ..kinetics import KineticContainer, Msd

# What should I do with THERMO_IN, THERMO_OUT - ?
THERMO_OUT = {'step': 'Step'}
THERMO_IN = {'step': 'step'}

class LammpsPot:
    """Lammps potential
    """

    _is_safe_to_serialize = True

    def __init__(self):
        pass

    @staticmethod
    def load(path, species = None, pair_style = None):
        f = path
        if isinstance(f, pathlib.Path): f = str(f)
        try:
            if isinstance(f, str): f = open(path, 'r')

            pot = LammpsPot()
            pot.data = f.read()
            if species is not None:
                pot.species = [ptable.NUMBERS[t] if isinstance(t, str) else t for t in species]
            else:
                pot.species = None
            pot.pair_style = pair_style
            return pot
        finally:
            if isinstance(f, io.IOBase) and not f.closed:
                f.close()

    @property
    def elements(self):
        return None if self.species is None else [ptable.ELEMENTS[t] for t in self.species]

    @elements.setter
    def elements(self, new_elements):
        self.species = [ptable.NUMBERS[t] if isinstance(t, str) else t for t in new_elements]

    def dump_str(self):
        return self.data

    def dump_for_lammps(self, species = None):
        if not species: species = self.species
        species = [ptable.NUMBERS[t] if isinstance(t, str) else t for t in species]
        if species != self.species:
            raise NotImplementedError('LammpsPot cannot be created, but then called for different species')
        elem_str = ' '.join([ptable.ELEMENTS[t] for t in species])
        files = {}
        pot_str = self.dump_str()
        pot_filename = f'pot_{hashlib.sha256(pot_str.encode()).hexdigest()}.lmp_pot'
        files[pot_filename] = pot_str
        pot_spec = f'''\
pair_style {self.pair_style}
pair_coeff * * {pot_filename} {elem_str}'''
        return {'pot_spec':pot_spec, 'files':files}

    def __repr__(self):
        if not hasattr(self, 'data'):
            return f'LammpsPot()'
        return f"<LammpsPot object at {hex(id(self))}>"

class GenericLammps(FileJob):
    """Generic LAMMPS calculation 

    Usage: ::

      with('lammps_script.in', 'r') as f: script = f.read()
      with('pot.eam.fs', 'r') as f: pot = f.read()
      job = GenericLammps(lammps_script = script, extra_in_files = {'pot.eam.fs': pot, ...}, extra_out_files = {'my_md.dump': str, ...})

    or simply::

      job = GenericLammps(script, {'pot.eam.fs': pot}, {'my_md.dump': str}).

    :param lammps_script: A string with the lammps script file contents
    :type lammps_script: str

    :param extra_in_files: same as the ``FileJob``'s ``in_files`` param
    :type extra_in_files: typically list or dict

    :param extra_out_files: same as the ``FileJob``'s ``out_files`` param
    :type extra_out_files: typically list or dict

    :param selected_al_reader: UNUSED: A function (or other callable object) that reads
      the selected configurations during active learning. Should be converts the selected configuration file content into 
      and ``extra_out_files`` are exactly like ``FileJob``'s ``out_files``.

    The job output will be a dictonary like ``{filename: contents}``, where
    filename can be ``'stdout'``, ``'stdin'``, ``'lammps_log'`` plus those given in ``extra_out_files``.
    In ``extra_out_files`` str means that the file should be read in a textual format (``bytes`` would mean binary format).
    """
    def lammps_run():
        from atomicasoft.jobs import job_info
        import atomicasoft.core.resources as resources
        if 'n_cores' not in job_info('metadata'):
            raise RuntimeError('run LAMMPS with run_job type of command')
        n_cores = job_info('metadata')['n_cores']
        stdout, stderr = resources.lammps_mpi.run(n_cores, 'lammps_script', ['-log', 'lammps_log'])
        return {'stdout':stdout, 'stderr':stderr}

    # TODO: use selected_al_reader
    def __init__(self, lammps_script: str, extra_in_files = {}, extra_out_files = {}, selected_al_reader = None):
        super().__init__(GenericLammps.lammps_run, in_files = extra_in_files, out_files = extra_out_files)
        self.resources.add('lammps_mpi')
        self.in_files['lammps_script'] = lammps_script
        self.out_files['lammps_log'] = str

class EnsembleNvtLangevin:
    _is_safe_to_serialize = True
    def __init__(self, temperature: float, temperature_mix_time = 0.1):
        self.temperature = temperature
        self.temperature_mix_time = temperature_mix_time
    def lammps_str(self, seed = None, cfg = None, pot = None):
        import random
        if seed is None:
            seed = random.randint(1,100000000)
        return f'''\
fix 1 all nve
fix 2 all langevin {self.temperature} {self.temperature} {self.temperature_mix_time} {seed}'''

class EnsembleNptLangevin:
    _is_safe_to_serialize = True
    def __init__(self, temperature: float, pressure: float = 0.0001, temperature_mix_time = 0.1, pressure_mix_time = 0.5):
        self.temperature = temperature
        self.pressure = pressure
        self.temperature_mix_time = temperature_mix_time
        self.pressure_mix_time = pressure_mix_time
    def lammps_str(self, seed = None, cfg = None, pot = None):
        import random
        if seed is None:
            seed = random.randint(1,100000000)
        pressure = self.pressure / Pressure.lammps_unit_convevt
        return f'''\
fix 1 all nph iso {pressure} {pressure} {self.pressure_mix_time} mtk yes
fix 2 all langevin {self.temperature} {self.temperature} {self.temperature_mix_time} {seed}'''

class EnsembleMuptLangevin:
    _is_safe_to_serialize = True
    def __init__(self, mu: list, temperature: float, pressure: float = 0.0001,
                 swap_species = None,
                 temperature_mix_time = 0.1, pressure_mix_time = 0.5,
                 n_md_steps = 45, n_mc_steps_multiplier = 1.0):
        assert type(mu) is list
        self.swap_species = swap_species
        self.mu = mu
        self.temperature = temperature
        self.pressure = pressure
        self.temperature_mix_time = temperature_mix_time
        self.pressure_mix_time = pressure_mix_time
        self.n_md_steps = n_md_steps
        self.n_mc_steps_multiplier = n_mc_steps_multiplier
    def lammps_str(self, seed = None, cfg = None, pot = None):
        import random, numpy as np
        if seed is None:
            seed = random.randint(1,100000000)
        if self.swap_species is None:
            self.swap_species = pot.species
        # convert to relative atomic types
        species_map = {t:i for i,t in enumerate(pot.species)}
        swap_rel_species = [species_map[s] for s in self.swap_species]
        pressure = self.pressure / Pressure.lammps_unit_convevt
        n_mc_steps = int(np.ceil(self.n_mc_steps_multiplier * cfg.n_atoms))
        n_atom_types = np.unique(cfg.types)
        atom_type_str = ' '.join([str(1+_) for _ in swap_rel_species])
        mu_str = ' '.join([str(_) for _ in self.mu])
        return f'''\
fix 1 all nph iso {pressure} {pressure} {self.pressure_mix_time} mtk yes
fix 2 all langevin {self.temperature} {self.temperature} {self.temperature_mix_time} {seed}
fix 3 all atom/swap {self.n_md_steps} {n_mc_steps} {seed} {self.temperature} ke yes semi-grand yes types {atom_type_str} mu {mu_str}'''


#        current_directory = pathlib.Path.cwd()
#        selected_cfg = []
        #matching_files = current_directory.glob('selected_cfg')
        #for file_path in matching_files:
            #selected_cfg += self.selected_al_reader()

class LammpsTrajectory(AnyJob):
    """Lammps NVT job, accumulating energy and pressure statistics over runs
    
    Typical usage: ::

      pot = atomicasoft.core.lammps_pot.LammpsPot.load('Al_mm.eam.fs', ['Al'], 'eam/fs')
      cfg = ...
      
      job = LammpsNvt(pot, cfg, temperature = 900, n_steps = 5000)
      job = jr.run_job(job, metadata = {'n_cores_min': 10, 'n_cores_max': 128})
      # job now has 50 rows of statitics on energy and pressure
      job = jr.run_job(job, metadata = {'n_cores_min': 10, 'n_cores_max': 128})
      # job now has 100 rows of statitics on energy and pressure
      
    ``n_steps`` can be passed directly into run_job: ::
    
      # this makes extra 1000 steps:
      job = jr.run_job(job, 1000, metadata = {'n_cores_min': 10, 'n_cores_max': 128})
      
    ``job.n_steps``, ``job.temperature``, etc., can in principle be changed between runs.
    job.series is an atomicasoft.core.series.TimeSeries object that contains two columns: energy and pressure

    :param cfg: starting (current) configuration
    :type cfg: atomicasoft.core.Cfg

    :param temperature: temperature in Kelvin
    :type temperature: float

    :param n_steps: TODO: update... number of steps, must be divisible by batch_size (see below)
    :type n_steps: int

    :param velocities: array of initial (current) velocities, defaults to None which makes them initialized according to the temperature
    :type metadata: np.ndarray, optional

    :param n_steps: number of time steps in a batch (each batch of time steps results into one row of statistics), defaults to 100
    :type n_steps: int, optional

    :param timestep: time step in ps, defaults to 1e-3 (= 1 fs)
    :type timestep: float, optional

    :param thermostat_mix_time: thermostat mix time in ps, defaults to 0.1 (= 100 fs)
    :type thermostat_mix_time: float, optional

    :param accurate_nbh_list: whether request building neighbor lists on every time step, defaults to True
    :type accurate_nbh_list: bool, optional   

    :param pot: interatomic potential. Can be hashed, i.e., wrapped into atomicasoft.core.Hasher
    :type pot: an atomicasoft.core potential
    
    """

    _is_safe_to_serialize = True
    
    # TODO: use selected_cfg_converter
    def __init__(self,
                 cfg,
                 ensemble,
                 pot = None,
                 velocities = None,
                 batch_size = 100,
                 n_steps = 1000,
                 timestep = 0.001,
                 accurate_nbh_list = True, selected_cfg_converter = None,
                 td_terms = [Term({Pressure(): 1}), Term({Energy(): 1})],
                 kinetic_terms = []):  # kinetic_terms = [Msd]
        self.metadata['needs_dir'] = True
        self.resources.add('lammps_mpi')
        self.accurate_nbh_list = accurate_nbh_list
        self.td_terms = TermContainer(td_terms)
        self.kinetic_terms = None if kinetic_terms is None else KineticContainer(kinetic_terms)
        self.kinetic_output = None
        self.selected_cfg_converter = selected_cfg_converter
        self.pot = pot
        self.n_steps = n_steps

        self.cfg = cfg
        self.ensemble = ensemble
        # self.seed = random.randint(1, 10**9) if seed is None else seed
        self.batch_size = batch_size
        self.timestep = timestep
        self.accurate_nbh_list = accurate_nbh_list
        
        self.velocities = velocities
        if self.velocities is None:
            k_Boltzmann = 0.831446
            n_atoms = len(cfg.pos)
            self.velocities = np.zeros( (n_atoms,3) )
            for i in range(n_atoms):
                self.velocities[i] = np.random.normal(0, np.sqrt(k_Boltzmann * ensemble.temperature / atomicasoft.core.ptable.MASSES[cfg.types[i]]), 3)

        # time series for energy and pressure
        self.series = atomicasoft.core.series.TimeSeries(self.td_terms.len)

    def __call__(self, pot = None, n_steps = None):
        import atomicasoft.core

        if pot is None:
            pot = self.pot
            if pot is None:
                raise TypeError('interatomic potential not given')

        if n_steps is None:
            n_steps = self.n_steps
            if n_steps is None:
                raise TypeError('interatomic potential not given')

        assert n_steps % self.batch_size == 0, f'n_steps should be divisible by batch_size (n_steps = {n_steps}, batch_size = {self.batch_size})'
        n_batches = n_steps // self.batch_size
        
        if isinstance(pot, atomicasoft.core.Hasher):
            pot = pot.data
        
        types = pot.species

        group_str = '\n'.join([f'group group_type_{i} type {i+1}' for i in range(len(types))])
    
        pot_data = pot.dump_for_lammps()
        pot_str = pot_data['pot_spec']

        mass_str = [f'mass {1+i} {atomicasoft.core.ptable.MASSES[t]} # {atomicasoft.core.ptable.ELEMENTS[t]}' for i,t in enumerate(types)]
        mass_str = '\n'.join(mass_str)
        
        neighbor_list_str = 'neighbor 0.1 bin\nneigh_modify delay 0 every 1 check yes' if self.accurate_nbh_list else ''
        
        ensemble_str = self.ensemble.lammps_str(cfg = self.cfg, pot = pot)
        
        datafile = atomicasoft.core.cfg.LammpsDatafile(self.cfg, self.velocities, types = types)
        thermo_var_names = []
        
        # returns dict with attributes: 'vars_instant', 'fixes', 'vars_aver'
        thermo_code = self.td_terms.lammps_thermo_code(batch_size = self.batch_size)
        
        thermo_var_names += [f'v_{term.lammps_var_name}_' for term in self.td_terms.terms]
        
        if self.kinetic_terms is None:
            kinetic_code = {'computes': '', 'vars_after_fixes': ''} 
        else:
            kinetic_code = self.kinetic_terms.lammps_kinetic_code(batch_size = self.batch_size)
            thermo_var_names += [f'v_{term.lammps_var_name}_' for term in self.kinetic_terms.terms]
            # kitetic_style = ' '.join([f'c_{term.lammps_compute_name}[4]' for term in self.kinetic_terms.terms])
            # kinetic_code['output'] = f'fix kinetic_output all ave/time {self.batch_size} 1 {self.batch_size} {kitetic_style} file "kinetic_output"'
        
        thermo_style = (f'custom {THERMO_IN["step"]} ' + 
                        ' '.join(thermo_var_names))
        thermo_modify = ' '.join(['%1.16g' for _ in thermo_var_names])


        str_script = f'''\
units       metal
atom_style  atomic
boundary    p p p

read_data   start_cfg.inp

{group_str}

{mass_str}

{pot_str}

{neighbor_list_str}

{thermo_code['vars_before_fixes']}

{ensemble_str}

timestep {self.timestep}

{thermo_code['fixes']}
{kinetic_code['computes']}

{thermo_code['vars_after_fixes']}
{kinetic_code['vars_after_fixes']}

thermo {self.batch_size}
thermo_style {thermo_style}
thermo_modify format line "%d {thermo_modify}"

print "HERE_IS_WHERE_THE_RUN_STARTS"
run {self.batch_size * n_batches}

write_data end_cfg.inp
'''
        extra_in_files = {'start_cfg.inp':datafile, **pot_data['files']}
        extra_out_files = {'end_cfg.inp':str}
        if hasattr(pot, 'al_enabled') and pot.al_enabled:
            selected_cfg_filename = pot_data['selected_cfg_filename']
            extra_out_files[selected_cfg_filename] = bytes
        if self.kinetic_terms is not None:
            extra_out_files['kinetic_output'] = str
        job = GenericLammps(str_script,
                            extra_in_files = extra_in_files,
                            extra_out_files = extra_out_files)
        job_result = job()

        # check if active learning was triggered
        if hasattr(pot, 'al_enabled') and pot.al_enabled:
            if job_result[selected_cfg_filename]:
                cfgs = pot.cfg_converter(job_result[selected_cfg_filename])
                raise ActiveLearningException(cfgs=cfgs)

        import io
        self.cfg, self.velocities = atomicasoft.core.cfg.ReadLammpsDatafile(io.StringIO(job_result['end_cfg.inp']), species = types)
        
        self.kinetic_output = np.zeros(shape=(n_batches,len(self.kinetic_terms.terms)))

        result_lines = job_result['lammps_log'].splitlines()
        starts_at = result_lines.index('HERE_IS_WHERE_THE_RUN_STARTS')
        line_iterator = iter(result_lines[starts_at:])
        l = next(line_iterator)
        while not re.match(f'\\s*{THERMO_OUT["step"]}',l):
            l = next(line_iterator)
        # first line does not matter
        l = next(line_iterator)
        for i in range(n_batches):
            l = next(line_iterator)
            nums = l.split()
            assert(int(nums[0]) == self.batch_size * (1+i))
            num_ind = 1
            with open('log', 'a') as f:
                f.write(f"{[float(nums[num_ind+j]) * term.const_lammps_unit_convert for j, term in enumerate(self.td_terms.terms)]}\n")
            self.series.append([float(nums[num_ind+j]) * term.const_lammps_unit_convert for j, term in enumerate(self.td_terms.terms)])
            num_ind += len(self.td_terms.terms)
            self.kinetic_output[i,:] = [float(nums[num_ind+j]) for j, term in enumerate(self.kinetic_terms.terms)]
        
        return self

class EnsembleAverage(AnyJob):
    _is_safe_to_serialize = True
    def __init__(self, TrajectoryJob, n_trajectories, cfg, ensemble,
                 velocities = None, batch_size = 100, timestep = 0.001,
                 accurate_nbh_list = True,
                 td_terms = [Term({Pressure(): 1}), Term({Energy(): 1})],
                 ar1_threshold = 0.1):
        self.accurate_nbh_list = accurate_nbh_list
        self.td_terms = TermContainer(td_terms)
        self.timestep = timestep
        self.batch_size = batch_size
        self.cfg = cfg
        self.ensemble = ensemble
        self.n_trajectories = n_trajectories
        self.ar1_threshold = ar1_threshold

        self.job_array = []
        for n in range(n_trajectories):
            job = TrajectoryJob(cfg = self.cfg, ensemble = self.ensemble, velocities = velocities, batch_size = batch_size, timestep = timestep, 
                                accurate_nbh_list = accurate_nbh_list, td_terms = td_terms)
            self.job_array.append(job)
        
        self.n_batches = 200 // self.n_trajectories # 400 to have the rho_err to be approx. 0.5

    # __call__ increases the trajectory size two-fold, so that the error reduces by a factor of sqrt(2) (~1.4)
    def __call__(self, pot):
        import atomicasoft.core.series
        import atomicasoft.jobs

        self.n_batches *= 2
        job_array_to_run = [{'job_func': job, 'job_kwargs': {'pot':pot, 'n_steps': self.batch_size * (self.n_batches - len(job.series.data))}} for job in self.job_array]

        self.job_array = atomicasoft.jobs.run_job_array(job_array_to_run)
        self.ar = atomicasoft.core.series.AutoRegr([job.series for job in self.job_array])
        while np.any(np.array(self.ar.rho_val) > self.ar1_threshold):
            self.batch_size *= 2
            for job in self.job_array:
                job.series.reduce_by(2)
                job.batch_size *= 2
            self.n_batches = max(400 // self.n_trajectories, (self.n_batches+1) // 2)
            # print(f'Keep going, n_batches = {self.n_batches}, batch_size = {self.batch_size}, rho: {self.ar.rho_val[0]} ± {self.ar.rho_err[0]}')

            job_array_to_run = [{'job_func': job, 'job_kwargs': {'pot':pot, 'n_steps': self.batch_size * (self.n_batches - len(job.series.data))}} for job in self.job_array]
            self.job_array = atomicasoft.jobs.run_job_array(job_array_to_run)
            self.ar = atomicasoft.core.series.AutoRegr([job.series for job in self.job_array])
        self.result = {term:Valerr(self.ar.mean_val[i], self.ar.mean_err[i]) for i,term in enumerate(self.td_terms.terms)}
        return self
