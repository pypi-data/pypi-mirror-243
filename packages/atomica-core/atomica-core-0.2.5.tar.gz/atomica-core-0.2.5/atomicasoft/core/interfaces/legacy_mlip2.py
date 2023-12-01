"""Interface with the legacy mlip-2 package

"""

import re, json, numpy as np, warnings, hashlib, string, random, io, pathlib

from .. import ptable
from .. import cfg
from .. import calc_cfg
from .. import relax_cfg
from .. import data_errors
from ..basic import temp_file_path
from .. import resources

from ..jobs._basic import *
from ..data_errors import FittingErrors

def _read_tag(line, tag_name, tag_type = str):
    tag = re.match(f'\\s*{tag_name}\\s*=\\s*(.*)\\s*$', line)
    #print(f'\\s*{tag_name}\\s*=\\s*(.*)\\s*$', line, tag)
    if not tag: return None
    return tag_type(tag.group(1))

def _read_flag(line, flag_name):
    flag = re.match(f'\\s*{flag_name}\\s*$', line)
    return bool(flag)

def _dumps_single_calc_cfg(calc, *, species = None) -> str:
    """Converts calc to the legacy-mlip2 format
    if species is given then it maps correspondingly the absolute to the relative species numbers.
    The typical use is dumps_calc_cfg(calc, species = mtp.species)
    """

    cfg = calc.cfg

    # preprocess: convert to relative species
    if cfg.types is None:
        types = None
    elif species:
        if isinstance(species[0], str):
            species = np.array([ptable.NUMBERS[t] for t in species])
        reverse_species = {s:i for i,s in enumerate(species)}
        types = [reverse_species[t] for t in cfg.types]
    else:
        types = cfg.types

    cell_str = '\n'.join([f'    {v[0]!r} {v[1]!r} {v[2]!r}' for v in cfg.cell])
    if cell_str:
        cell_str = f'  SuperCell\n{cell_str}'
    
    tag_str = f'  AtomData: id{" type" if types is not None else " "} cartes_x cartes_y cartes_z'
    if hasattr(calc, 'forces'):
        tag_str += ' fx fy fz'
    atom_str = ''
    for i in range(cfg.n_atoms):
        atom_str += f'\n    {i+1}'
        if types is not None: atom_str += f' {types[i]}'
        atom_str += f' {cfg.pos[i][0]!r} {cfg.pos[i][1]!r} {cfg.pos[i][2]!r}'
        if hasattr(calc, 'forces'):
            atom_str += f' {calc.forces[i][0]!r} {calc.forces[i][1]!r} {calc.forces[i][2]!r}'
    trailing_str = ''
    if hasattr(calc, 'energy'):
        trailing_str += f'\n  Energy\n    {calc.energy!r}'
    if hasattr(calc, 'stress'):
        stress6 = calc.stress.vector
        trailing_str += f'\n  PlusStress: xx yy zz yz xz xy\n    {stress6[0]!r} {stress6[1]!r} {stress6[2]!r} {stress6[3]!r} {stress6[4]!r} {stress6[5]!r}'
    ret = f'''\
BEGIN_CFG
  Size
   {cfg.n_atoms}
{cell_str}
{tag_str}{atom_str}{trailing_str}
END_CFG
'''
    return ret

def dumps_cfg(what, *, species = None) -> str:
    if not isinstance(what, list):
        what = [what]
    ret_str = ""
    for c in what:
        if isinstance(c, cfg.Cfg):
            ret_str += _dumps_single_calc_cfg(calc_cfg.CalcCfg(cfg = c), species = species)
        else:
            ret_str += _dumps_single_calc_cfg(c, species = species)
        ret_str += '\n'
    return ret_str

def load_json(json_stream, *, species = None):
    """Load the output of mlp convert-cfg --output-format=json

    Can return either a CalcCfg object or a list of CalcCfg objects
    """
    if species:
        if isinstance(species[0], str):
            species = np.array([ptable.NUMBERS[t] for t in species])
    else:
        species = None

    cfg_list = json.load(json_stream)
    if not isinstance(cfg_list, list):
        cfg_list = [cfg_list]
    for i, json_obj in enumerate(cfg_list):
        types = json_obj['types']
        if species is not None:
            types = [species[t] for t in types]
        calc_cfg_ = calc_cfg.CalcCfg(cfg = cfg.Cfg(cell = json_obj['cell'], pos = json_obj['pos'], types = types))
        if 'energy' in json_obj: calc_cfg_.energy = json_obj['energy']
        if 'forces' in json_obj: calc_cfg_.forces = np.array(json_obj['forces'])
        if 'stress' in json_obj: calc_cfg_.stress = calc_cfg.Stress(json_obj['stress'])
        cfg_list[i] = calc_cfg_
    if len(cfg_list) == 1: return cfg_list[0]
    else: return cfg_list

def loads_json(json_str: str, *, species = None):
    return load_json(io.StringIO(json_str), species = species)

def loads_cfg(cfg_str, *, species = None) -> str:
    """Converting the cfg_str in native MLIP-2 format to the json format

    cfg_str can either be of type `str` or `bytes`
    """
    temp_in_file = temp_file_path()
    temp_out_file = temp_file_path()

    mode = 'wb' if isinstance(cfg_str, bytes) else 'w'
    with open(temp_in_file, mode) as f:
        f.write(cfg_str)

    resources.mlip2_mpi.run(
        n_cores = 1,
        params_list = ['convert-cfg',
                       str(temp_in_file),
                       str(temp_out_file),
                       '--output-format=json'
                      ])
    with temp_out_file.open() as f:
        ret = load_json(f, species = species)
    temp_in_file.unlink()
    temp_out_file.unlink()
    return ret

class AlMaxvol:
    """Container for Maxvol parameters and state

    :param threshold: selection threshold. Default is 2.0
    :type threshold: float

    :param threshold_break: breaking threshold. By default is set to threshold
    :type threshold_break: float

    :param selected_cfg_filename: (UNUSED, TO DELETE) filename where the potential will save the selected configurations
    :type selected_cfg_filename: str

    :param state: active learning state
    :type state: bytes or None

    :ivar threshold: selection threshold
    :vartype threshold: float

    :ivar threshold_break: breaking threshold
    :vartype threshold_break: float

    :ivar selected_cfg_filename: (UNUSED, TO DELETE) filename where the potential will save the selected configurations
    :vartype selected_cfg_filename: str

    :ivar state: active learning state
    :vartype state: bytes or None

    """
    _is_safe_to_serialize = True
    def __init__(self, *, threshold = 2.0, threshold_break = None, selected_cfg_filename = 'selected_cfg', state = None):
        if threshold_break is None:
            threshold_break = threshold
        self.threshold = threshold
        self.threshold_break = threshold_break
        self.selected_cfg_filename = selected_cfg_filename
        self.state = state

    def __repr__(self):
        return f"<maxvol active learning object, threshold = {self.threshold}, threshold_break = {self.threshold_break}>"

class Mtp(AnyJob):
    """MTP potential from the MLIP-2 package

    Sample usage: ::

      pot = Mtp.load('trained.mtp', species = ['Pd','Ag'])

    There also can be `pot.als` which is the active learning state and `pot.al_enabled:bool`
    which is set to `True` when `pot.als` is set, but `pot.al_enabled:bool` can be explicitly set to `False`.


    """

    _is_safe_to_serialize = True

    def __init__(self): #initializer
        self._al = None
        self.metadata['needs_dir'] =  True
        self.resources.add('mlip2_mpi')

    def calc_cfg(self, cfg_set):
        from atomicasoft.core import Cfg
        import atomicasoft.core.interfaces.legacy_mlip2 as legacy_mlip2

        if isinstance(cfg_set, Cfg):
            cfg_set = [cfg_set]
        
        cfg_set_str = legacy_mlip2.dumps_cfg(cfg_set, species = self.species)
        job = GenericMlip2([['calc-efs','pot.mtp','in.cfg','out.cfg'],
                                   ['convert-cfg','out.cfg','out.json','--output-format=json']],
                                  in_files = {'in.cfg': cfg_set_str, 'pot.mtp': self.dump_str()},
                                  out_files = {'out.json': str})
        result = job()
        return legacy_mlip2.loads_json(result['out.json'], species = self.species)
    calc_cfg.metadata = {'needs_dir': True}
    calc_cfg.resources = {'mlip2_mpi'}

    def relax_cfg(self,
                  cfg_set,
                  n_steps_max = 80,
                  force_tolerance = 1e-4,
                  stress_tolerance = 1e-3,
                  constraints = False,
                  keep_only_last = True): # qwe
        if not keep_only_last:
            raise TypeError('only keep_only_last = True is implemented')
        from atomicasoft.core import Cfg
        import atomicasoft.core.interfaces.legacy_mlip2 as legacy_mlip2

        if isinstance(cfg_set, Cfg):
            cfg_set = [cfg_set]
        
        cfg_set_str = legacy_mlip2.dumps_cfg(cfg_set, species = self.species)
        mlip_ini_str, files, selected_cfg_filename = self._generate_mlip_ini('pot.mtp')
        files['mlip.ini'] = mlip_ini_str
        out_files = {'out.json': str}
        extra_merge_commands = []
        if selected_cfg_filename:
            out_files[selected_cfg_filename] = str
            extra_merge_commands.append(['merge-cfg',selected_cfg_filename]) # this is not a bug: it should be a list of lists
        extra_relax_opts = []
        if constraints: extra_relax_opts.append('--stress-tolerance=0')
        job = GenericMlip2([['relax','mlip.ini', '--cfg-filename=in.cfg', '--save-relaxed=out.cfg',
                             '--save-unrelaxed=unrelaxed.cfg',
                             f'--iteration-limit={n_steps_max}',
                             f'--force-tolerance={force_tolerance}',
                             f'--stress-tolerance={stress_tolerance}',
                             *extra_relax_opts],
                            ['merge-cfg','out.cfg'],
                            *extra_merge_commands,
                            ['convert-cfg','out.cfg','out.json','--output-format=json']],
                           in_files = {'in.cfg': cfg_set_str, 'pot.mtp': self.dump_str(), **files},
                           out_files = out_files)
        job_result = job()

        # check if active learning was triggered
        if self.al_enabled:
            if job_result[selected_cfg_filename]:
                cfgs = self.cfg_converter(job_result[selected_cfg_filename])
                raise ActiveLearningException(cfgs=cfgs)

        return legacy_mlip2.loads_json(job_result['out.json'], species = self.species)
    relax_cfg.metadata = {'needs_dir': True}
    relax_cfg.resources = {'mlip2_mpi'}


    @staticmethod
    def load(path, species = None):
        f = path
        if isinstance(f, pathlib.Path): f = str(f)
        try:
            if isinstance(f, str): f = open(path, 'r')

            mtp = Mtp()

            # read "MTP"
            l = f.readline()
            if _read_flag(l, 'MTP') is None:
                raise ValueError('The given file is not an MTP file')

            # read "version = 1.1.0"
            l = f.readline()
            if _read_flag(l, 'version = 1.1.0') is None:
                raise ValueError('unsupported MTP version: only 1.1.0 is supported')

            # read "potential_name = MTP1m"
            l = f.readline()
            mtp.potential_name = _read_tag(l, 'potential_name')
            if mtp.potential_name is None:
                raise ValueError('potential_name not given')

            # try to read "scaling"
            l = f.readline()
            tag = _read_tag(l, 'scaling', float)
            if tag is not None:
                mtp.scaling = tag
                l = f.readline()

            # read "species_count"
            mtp.species_count = _read_tag(l, 'species_count', int)
            if mtp.species_count is None:
                raise ValueError('species_count not given')
            
            # read "potential_tag"
            l = f.readline()
            mtp.potential_tag = _read_tag(l, 'potential_tag')
            if mtp.potential_tag is None:
                raise ValueError('potential_tag not given')
            
            # read "radial_basis_type"
            l = f.readline()
            mtp.radial_basis_type = _read_tag(l, 'radial_basis_type')
            if mtp.radial_basis_type is None:
                raise ValueError('radial_basis_type not given')
            
            # read "min_dist"
            l = f.readline()
            mtp.min_dist = _read_tag(l, 'min_dist', float)
            if mtp.min_dist is None:
                raise ValueError('min_dist not given')

            # read "max_dist"
            l = f.readline()
            mtp.max_dist = _read_tag(l, 'max_dist', float)
            if mtp.max_dist is None:
                raise ValueError('max_dist not given')
            
            # read "radial_basis_size"
            l = f.readline()
            mtp.radial_basis_size = _read_tag(l, 'radial_basis_size', int)
            if mtp.radial_basis_size is None:
                raise ValueError('radial_basis_size not given')
            
            # read "radial_funcs_count"
            l = f.readline()
            mtp.radial_funcs_count = _read_tag(l, 'radial_funcs_count', int)
            if mtp.radial_funcs_count is None:
                raise ValueError('radial_funcs_count not given')

            # trained potentials have radial_coeffs        
            l = f.readline()
            if _read_flag(l, 'radial_coeffs'):
                try:
                    mtp.radial_coeffs = np.zeros((mtp.species_count, mtp.species_count, mtp.radial_funcs_count, mtp.radial_basis_size))
                    for i in range(mtp.species_count):
                        for j in range(mtp.species_count):
                            l = f.readline()
                            assert _read_flag(l, f'{i}-{j}')
                            for k in range(mtp.radial_funcs_count):
                                l = f.readline()
                                l = l.replace('{', '[')
                                l = l.replace('}', ']')
                                mtp.radial_coeffs[i][j][k] = json.loads(l)
                    l = f.readline()
                except:
                    raise ValueError('error reading radial_coeffs')

            # reading alpha_moments_count
            mtp.alpha_moments_count = _read_tag(l, 'alpha_moments_count', int)
            if mtp.alpha_moments_count is None:
                raise ValueError('alpha_moments_count not given')

            # reading alpha_index_basic_count
            l = f.readline()
            mtp.alpha_index_basic_count = _read_tag(l, 'alpha_index_basic_count', int)
            if mtp.alpha_index_basic_count is None:
                raise ValueError('alpha_index_basic_count not given')
            
            # reading alpha_index_basic
            l = f.readline()
            mtp.alpha_index_basic = _read_tag(l, 'alpha_index_basic')
            if mtp.alpha_index_basic is None:
                raise ValueError('alpha_index_basic not given')

            # reading alpha_index_times_count
            l = f.readline()
            mtp.alpha_index_times_count = _read_tag(l, 'alpha_index_times_count', int)
            if mtp.alpha_index_times_count is None:
                raise ValueError('alpha_index_times_count not given')
            
            # reading alpha_index_times
            l = f.readline()
            mtp.alpha_index_times = _read_tag(l, 'alpha_index_times')
            if mtp.alpha_index_times is None:
                raise ValueError('alpha_index_times not given')

            # reading alpha_scalar_moments
            l = f.readline()
            mtp.alpha_scalar_moments = _read_tag(l, 'alpha_scalar_moments', int)
            if mtp.alpha_scalar_moments is None:
                raise ValueError('alpha_scalar_moments not given')
            
            # reading alpha_moment_mapping
            l = f.readline()
            mtp.alpha_moment_mapping = _read_tag(l, 'alpha_moment_mapping')
            if mtp.alpha_moment_mapping is None:
                raise ValueError('alpha_moment_mapping not given')

            # reading rest of the coeffs
            try:
                l = f.readline()
                tag = _read_tag(l, 'species_coeffs')
                if tag:
                    tag = tag.replace('{', '[')
                    tag = tag.replace('}', ']')
                    mtp.species_coeffs = np.array(json.loads(tag))
                l = f.readline()
                tag = _read_tag(l, 'moment_coeffs')
                if tag:
                    tag = tag.replace('{', '[')
                    tag = tag.replace('}', ']')
                    mtp.moment_coeffs = np.array(json.loads(tag))
            except:
                pass
            f.close()
        finally:
            if isinstance(f, io.IOBase) and not f.closed:
                f.close()

        # postprocessing
        mtp.species = None
        if species is not None:
            mtp.species = species
        if mtp.species is None and mtp.potential_tag:
            mtp.species = mtp.potential_tag.split('_')
        if mtp.species:
            mtp.species = [ptable.NUMBERS[t] if isinstance(t, str) else t for t in mtp.species]
            mtp.potential_tag = '_'.join([ptable.ELEMENTS[t] for t in mtp.species])
            assert len(mtp.species) == mtp.species_count, 'Error: species information does not match species_count'
        else:
            warnings.warn('loading potential without species information')

        return mtp

    def is_trained(self):
        return hasattr(self, 'radial_coeffs')

    @property
    def al_enabled(self):
        return self._al is not None

    @property
    def al(self):
        return self._al

    @al.setter
    def al(self, new_al):
        self._al = new_al

    def cfg_converter(self, cfg_str):
        return loads_cfg(cfg_str, species = self.species)
    
    @property
    def elements(self):
        return None if self.species is None else [ptable.ELEMENTS[t] for t in self.species]

    @elements.setter
    def elements(self, new_elements):
        self.species = [ptable.NUMBERS[t] if isinstance(t, str) else t for t in new_elements]
    
    def _c_array(l):
        return '{' + ', '.join([format(elem) for elem in l]) + '}'

    def dump_str(self):
        if hasattr(self,'scaling'): scaling = f'scaling = {self.scaling}\n'
        else: scaling = ''
        if(self.is_trained()):
            radial_coeffs = '  radial_coeffs\n'
            for i in range(self.species_count):
                for j in range(self.species_count):
                    radial_coeffs += f'    {i}-{j}\n'
                    for k in range(self.radial_funcs_count):
                        radial_coeffs += '      ' + Mtp._c_array(self.radial_coeffs[i][j][k]) + '\n'
            species_coeffs = f'species_coeffs = {Mtp._c_array(self.species_coeffs)}\n'
            moment_coeffs = f'moment_coeffs = {Mtp._c_array(self.moment_coeffs)}\n'
        else:
            radial_coeffs = ''
            species_coeffs = ''
            moment_coeffs = ''
        return f'''\
MTP
version = 1.1.0
potential_name = {self.potential_name}
{scaling}species_count = {self.species_count}
potential_tag = {self.potential_tag}
radial_basis_type = {self.radial_basis_type}
  min_dist = {self.min_dist}
  max_dist = {self.max_dist}
  radial_basis_size = {self.radial_basis_size}
  radial_funcs_count = {self.radial_funcs_count}
{radial_coeffs}alpha_moments_count = {self.alpha_moments_count}
alpha_index_basic_count = {self.alpha_index_basic_count}
alpha_index_basic = {self.alpha_index_basic}
alpha_index_times_count = {self.alpha_index_times_count}
alpha_index_times = {self.alpha_index_times}
alpha_scalar_moments = {self.alpha_scalar_moments}
alpha_moment_mapping = {self.alpha_moment_mapping}
{species_coeffs}{moment_coeffs}'''

    @property
    def al_selected_cfg_filename(self) -> str:
        return "selected_cfg" if self.al_enabled else ""

    def _generate_mlip_ini(self, pot_filename):
        files = {}
        mlip_ini_str = f'''\
mtp-filename   {pot_filename}
select         {'TRUE' if self.al_enabled else 'FALSE'}
'''
        selected_cfg_filename = None
        if self.al_enabled:
            als_filename = f'{pot_filename}.als'
            random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=25))
            selected_cfg_filename = f'selected_cfg_{random_str}.cfg'
            al = self.al
            files[als_filename] = al.state
            mlip_ini_str += f'''\
  select:threshold          {al.threshold}
  select:threshold-break    {al.threshold_break}
  select:save-selected      {selected_cfg_filename}
  select:load-state         {als_filename}
'''        
        return mlip_ini_str, files, selected_cfg_filename

    def dump_for_lammps(self, species = None):
        if not species: species = self.species
        species = [ptable.NUMBERS[t] if isinstance(t, str) else t for t in species]
        if species != self.species:
            raise NotImplementedError('Species mapping not yet implemented')
        files = {}
        pot_str = self.dump_str()
        pot_sha256 = hashlib.sha256(pot_str.encode()).hexdigest()
        pot_filename = f'pot_{pot_sha256}.mtp'
        files[pot_filename] = pot_str

        mlip_ini_str, extra_files, selected_cfg_filename = self._generate_mlip_ini(pot_filename)
        files['mlip.ini'] = mlip_ini_str
        files = {**files, **extra_files}

        pot_spec = f'''\
pair_style mlip mlip.ini
pair_coeff * *'''
        return {'pot_spec':pot_spec, 'files':files, 'selected_cfg_filename': selected_cfg_filename}

    def __repr__(self):
        if not hasattr(self, 'species_count'):
            return f'Mtp()'
        str_trained = 'trained' if self.is_trained() else 'untrained'
        str_species = f'{self.species_count} unknown species' if self.species is None else f'{self.elements}'
        str_al_enabled = ', with active learning' if self.al_enabled else ''
        return f"<Mtp object '{self.potential_name}', {str_trained} for {str_species}{str_al_enabled}>"

class GenericMlip2(FileJob):
    r"""Generic MLIP-2 run 

    Simple usage: ::

      job = GenericMlip2(['help'])
      result = jr.run_job(job)
      print(result['stdout'].decode())

    More advanced usage (fitting a potential): ::

      train_set = [atomicasoft.core.calc_cfg.CalcCfg.read_vasp((p / 'vasprun.xml').open('r')) for p in (pathlib.Path() / 'vasp').iterdir()]
      train_set_str = '\n'.join([atomicasoft.core.legacy_mlip2.dumps_cfg(c, species = ['Pd', 'Ag']) for c in train_set])
      job = GenericMlip2(['train','init.mtp','train.cfg','--trained-pot-name=out.mtp'],
                                in_files = {'train.cfg': train_set_str, 'init.mtp': True},
                                out_files = {'out.mtp': str})
      result = jr.run_job(job, metadata = {'needs_dir': True, 'n_cores_min': 10, 'n_cores_max': 10})
      pot = atomicasoft.core.legacy_mlip2.Mtp.load(io.StringIO(result['out.mtp']), species = ['Pd', 'Ag'])

    ``in_files`` are exactly like ``FileJob``'s ``in_files``
    and ``out_files`` are exactly like ``FileJob``'s ``out_files``.

    The job output will be a dictonary like ``{filename: contents}``, where
    filename can be ``'stdout'``, ``'stdin'``, ``'lammps_log'`` plus those given in ``extra_out_files``.
    In ``extra_out_files`` str means that the file should be read in a textual format (``bytes`` would mean binary format).
    """
    @staticmethod
    def mlp_run(param_list = None):
        from atomicasoft.jobs import job_info
        import atomicasoft.core.resources as resources
        if param_list is None:
            param_list = self.param_list
        if 'n_cores' not in job_info('metadata'):
            raise RuntimeError('run MLIP-2 with run_job type of command')
        n_cores = job_info('metadata')['n_cores']
        if not isinstance(param_list[0], list):
            param_list = [param_list]
        for params in param_list:
            stdout, stderr = resources.mlip2_mpi.run(n_cores, params)
        return {'stdout':stdout, 'stderr':stderr}

    def __init__(self, param_list = [], in_files = {}, out_files = {}):
        super().__init__(GenericMlip2.mlp_run, args = (param_list,), in_files = in_files, out_files = out_files)
        self.param_list = param_list
        self.resources.add('mlip2_mpi')


def Mlip2FormatErrors(errors: FittingErrors) -> str:
    return f"""        * * * TRAIN ERRORS * * *

_________________Errors report_________________
Energy:
    Maximal absolute difference = {errors.energy.maxad}
    Average absolute difference = {errors.energy.mad}
    RMS     absolute difference = {errors.energy.rmsd}

Energy per atom:
    Maximal absolute difference = {errors.energy_per_atom.maxad}
    Average absolute difference = {errors.energy_per_atom.mad}
    RMS     absolute difference = {errors.energy_per_atom.rmsd}

Forces:
    Maximal absolute difference = {errors.forces.maxad}
    Average absolute difference = {errors.forces.mad}
    RMS     absolute difference = {errors.forces.rmsd}

Stresses (in eV):
    Maximal absolute difference = {errors.stress_ev.maxad}
    Average absolute difference = {errors.stress_ev.mad}
    RMS     absolute difference = {errors.stress_ev.rmsd}

Stresses (in GPa):
    Maximal absolute difference = {errors.stress.maxad}
    Average absolute difference = {errors.stress.mad}
    RMS     absolute difference = {errors.stress.rmsd}
_______________________________________________"""        


class Mlip2CalcErrors(AnyJob):
    """Class for errors calculation after MTP potenital fitting
    """
    def __init__(self, pot = None, db_set = None):
        self.metadata['needs_dir'] = True
        self.resources.append('mlip2_mpi')
        self.pot = pot
        self.db_set = db_set

    @staticmethod
    def _parse(error_string):
        errors = FittingErrors()
        current_quantity = None
        for line in error_string.split('\n'):
            line = line.strip()
            if line.startswith('Energy:'): current_quantity = errors.energy
            elif line.startswith('Energy per atom:'): current_quantity = errors.energy_per_atom
            elif line.startswith('Forces:'): current_quantity = errors.forces
            elif line.startswith('Stresses (in GPa):'): current_quantity = errors.stress
            elif line.startswith('Stresses (in eV):'): current_quantity = errors.stress_ev
            elif line.startswith('Maximal absolute difference'): current_quantity.maxad = float(line.split('=')[1].strip())
            elif line.startswith('Average absolute difference'): current_quantity.mad = float(line.split('=')[1].strip())
            elif line.startswith('RMS     absolute difference'): current_quantity.rmsd = float(line.split('=')[1].strip())
        return errors

    def __call__(self):
        import atomicasoft.core.interfaces.legacy_mlip2 as legacy_mlip2
        if isinstance(self.db_set, atomicasoft.core.Cfg):
            self.db_set = [self.db_set]

        db_set_str = legacy_mlip2.dumps_cfg(self.db_set, species = self.pot.species)
        job = GenericMlip2(['calc-errors', 'pot.mtp','db.cfg'],
                                  in_files = {'pot.mtp': self.pot.dump_str(), 'db.cfg': db_set_str})
        result = job()

        return self._parse(result['stdout'].decode())

class Mlip2Train(AnyJob):
    _is_safe_to_serialize = True
    
    def __init__(self, pot = None, train_set = None, active_learning = None):
        self.metadata['needs_dir'] = True
        self.resources.add('mlip2_mpi')
        self.pot = pot
        self.train_set = train_set
        self.active_learning = active_learning

    def __call__(self, pot = None, train_set = None, active_learning = None):
        from atomicasoft.jobs import job_info

        import subprocess
        import atomicasoft.core
        import atomicasoft.core.interfaces.legacy_mlip2 as legacy_mlip2
        import random

        if pot is None:
            pot = self.pot
        if isinstance(pot, atomicasoft.core.Hasher):
            pot = pot.data

        if train_set is None:
            train_set = self.train_set
        if isinstance(train_set, atomicasoft.core.Hasher):
            train_set = train_set.data

        if active_learning is None:
            active_learning = self.active_learning
        if active_learning is None:
            active_learning = pot.al
        if isinstance(active_learning, atomicasoft.core.Hasher):
            active_learning = active_learning.data
        
        train_set_str = legacy_mlip2.dumps_cfg(train_set, species = pot.species)
        job = GenericMlip2(['train','init.mtp','train.cfg','--trained-pot-name=out.mtp'],
                                  in_files = {'train.cfg': train_set_str, 'init.mtp': pot.dump_str()},
                                  out_files = {'out.mtp': str})
        result = job()
        pot = legacy_mlip2.Mtp.load(io.StringIO(result['out.mtp']), species = pot.species)

        if active_learning:
            job = GenericMlip2(['calc-grade','pot.mtp','train.cfg','train.cfg','temp.cfg','--als-filename=out.als'],
                                      in_files = {'train.cfg': train_set_str, 'pot.mtp': pot.dump_str()},
                                      out_files = {'out.als': bytes})
            n_cores = job_info('metadata')['n_cores']
            job_info('metadata')['n_cores'] = 1
            pot.al = active_learning
            pot.al.state = job()['out.als']
            job_info('metadata')['n_cores'] = n_cores
        return pot

class Mlip2ConstructActiveSet(AnyJob):
    _is_safe_to_serialize = True
    
    def __init__(self, pot = None, train_set = None, active_learning = None):
        self.metadata['needs_dir'] = True
        self.resources.add('mlip2_mpi')
        self.pot = pot
        self.train_set = train_set
        self.active_learning = active_learning

    def __call__(self, pot = None, train_set = None, active_learning = None):
        from atomicasoft.jobs import job_info

        import subprocess
        import atomicasoft.core
        import atomicasoft.core.interfaces.legacy_mlip2 as legacy_mlip2
        import random

        if pot is None:
            pot = self.pot
        if isinstance(pot, atomicasoft.core.Hasher):
            pot = pot.data

        if train_set is None:
            train_set = self.train_set
        if isinstance(train_set, atomicasoft.core.Hasher):
            train_set = train_set.data

        if active_learning is None:
            active_learning = self.active_learning
        if active_learning is None:
            active_learning = pot.al
        if isinstance(active_learning, atomicasoft.core.Hasher):
            active_learning = active_learning.data

        if not active_learning:
            raise TypeError('active_learning or pot.al should be given')

        train_set_str = legacy_mlip2.dumps_cfg(train_set, species = pot.species)

        job = GenericMlip2(['calc-grade','pot.mtp','train.cfg','train.cfg','temp.cfg','--als-filename=out.als'],
                                  in_files = {'train.cfg': train_set_str, 'pot.mtp': pot.dump_str()},
                                  out_files = {'out.als': bytes})
        n_cores = job_info('metadata')['n_cores']
        job_info('metadata')['n_cores'] = 1
        pot.al = active_learning
        pot.al.state = job()['out.als']
        job_info('metadata')['n_cores'] = n_cores

        return pot

class Mlip2SelectAdd(AnyJob):
    _is_safe_to_serialize = True
    
    def __init__(self, pot = None, train_set = None, extrapolative_cfgs = None):
        self.metadata['needs_dir'] = True
        self.resources.add('mlip2_mpi')
        self.pot = pot
        self.train_set = train_set
        self.extrapolative_cfgs = extrapolative_cfgs

    def __call__(self, pot = None, train_set = None, extrapolative_cfgs = None):
        from atomicasoft.jobs import job_info
        import atomicasoft.core
        import atomicasoft.core.interfaces.legacy_mlip2 as legacy_mlip2

        if pot is None:
            pot = self.pot
        if isinstance(pot, atomicasoft.core.Hasher):
            pot = pot.data

        if train_set is None:
            train_set = self.train_set
        if isinstance(train_set, atomicasoft.core.Hasher):
            train_set = train_set.data

        if extrapolative_cfgs is None:
            extrapolative_cfgs = self.extrapolative_cfgs
        if isinstance(extrapolative_cfgs, atomicasoft.core.Hasher):
            extrapolative_cfgs = extrapolative_cfgs.data

        train_set_str = legacy_mlip2.dumps_cfg(train_set, species = pot.species)
        extrapolative_set_str = legacy_mlip2.dumps_cfg(extrapolative_cfgs, species = pot.species)

        job = GenericMlip2(['select-add','pot.mtp','train.cfg','extrapolative.cfg','to_be_added.cfg'],
                                  in_files = {'train.cfg': train_set_str,
                                              'pot.mtp': pot.dump_str(),
                                              'extrapolative.cfg': extrapolative_set_str},
                                  out_files = {'to_be_added.cfg': str})
        n_cores = job_info('metadata')['n_cores']
        job_info('metadata')['n_cores'] = 1
        job_result = job()
        to_be_added = legacy_mlip2.loads_cfg(job_result['to_be_added.cfg'], species = pot.species)
        job_info('metadata')['n_cores'] = n_cores

        return to_be_added

class Mlip2CalcEfs(AnyJob):
    _is_safe_to_serialize = True
    
    def __init__(self, pot = None):
        self.metadata['needs_dir'] = True
        self.resources.add('mlip2_mpi')
        self.pot = pot

    def __call__(self, cfg_set):
        import atomicasoft.core
        import atomicasoft.core.interfaces.legacy_mlip2 as legacy_mlip2
        import json

        if isinstance(self.pot, atomicasoft.core.Hasher):
            self.pot = self.pot.data
        if isinstance(cfg_set, atomicasoft.core.Hasher):
            cfg_set = cfg_set.data
        if isinstance(cfg_set, atomicasoft.core.Cfg):
            cfg_set = [cfg_set]
        
        cfg_set_str = legacy_mlip2.dumps_cfg(cfg_set, species = self.pot.species)
        job = GenericMlip2([['calc-efs','pot.mtp','in.cfg','out.cfg'],
                                   ['convert-cfg','out.cfg','out.json','--output-format=json']],
                                  in_files = {'in.cfg': cfg_set_str, 'pot.mtp': self.pot.dump_str()},
                                  out_files = {'out.json': str})
        result = job()
        return legacy_mlip2.loads_json(result['out.json'], species = self.pot.species)
