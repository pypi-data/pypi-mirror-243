"""VASP jobs + quantum-mechanics
"""

import xmltodict, re, numpy as np, io

import logging
logger = logging.getLogger(__name__)

from .. import Cfg
from ..calc_cfg import CalcCfg
from ..jobs._basic import *

def _parse_i_logical(s: str):
    if(s[0] == 'F' or s[0] == 'f'): return False
    if(s[0] == 'T' or s[0] == 't'): return True
    raise ValueError('unknown logical expresion: ' + s)
_parse_i_func = {'int': int, 'logical': _parse_i_logical, 'float': float, 'string': str}

def _parse_to_lists(obj):
    if isinstance(obj, dict):
        for k in obj:
            if k in ['separator','i','v','r','varray','array']:
                if not isinstance(obj[k], list):
                    obj[k] = [obj[k]]
            _parse_to_lists(obj[k])
    elif isinstance(obj, list):
        for i in range(len(obj)):
            _parse_to_lists(obj[i])

def _parse_v(v):
    if isinstance(v, str):
        try:
            return [float(num) for num in v.split()]
        except ValueError:
            return None
    if isinstance(v, dict):
        try:
            return _parse_i_func[v.get('@type','float')](v.get('#text',''))
        except ValueError:
            return None

def _parse_array(a):
    if not '@dim' in a['dimension']:
        return 'unparsed'
    assert a['dimension']['@dim'] == '1'
    fields = []
    types = []
    for f in a['field']:
        if isinstance(f, str):
            fields.append(f)
            types.append('float')
        else:
            fields.append(f['#text'])
            types.append(f['@type'])
    l = []
    if not isinstance(a['set']['rc'], list): a['set']['rc'] = [a['set']['rc']]
    for c in a['set']['rc']:
        l.append({fields[i]:_parse_i_func[types[i]](e) for i,e in enumerate(c['c'])})
            
    return l

def _parse(obj):
    if isinstance(obj, dict):
        keys = list(obj.keys())
        while 'separator' in keys:
            l = obj['separator']
            del obj['separator']
            for e in l:
                del e['@name']
                for f in ['separator','i','v','r','varray', 'array']:
                    if f in e:
                        if not f in obj:
                            obj[f] = []
                        obj[f] += e[f]
            keys = list(obj.keys())
        if 'i' in keys:
            for e in obj['i']:
                obj[e['@name']] = _parse_i_func[e.get('@type','float')](e.get('#text',''))
            del obj['i']
        if 'array' in keys:
            for e in obj['array']:
                if '@name' in e:
                    obj[e['@name']] = _parse_array(e)
                else:
                    obj['array'] = _parse_array(e)
            del obj['array']
        if 'varray' in keys:
            for e in obj['varray']:
                obj[e['@name']] = np.array([_parse_v(v) for v in e['v']])
            del obj['varray']
        if 'v' in keys:
            for e in obj['v']:
                obj[e['@name']] = [float(num) for num in e.get('#text','').split()]
            del obj['v']

        for k in obj:
            _parse(obj[k])
    elif isinstance(obj, list):
        for i in range(len(obj)):
            _parse(obj[i])
    #if isinstance(obj, list):
    #    return parse_list(obj)
    return obj

def parse(obj):
    _parse_to_lists(obj)
    _parse(obj)

KEEP_PARAM_TAGS = set(('PREC','ENMAX','ENAUG','EDIFF','IALGO','NMIN','NGX','NGY','NGZ','NGXF','NGYF','NGZF','ADDGRID','ISIF','ISYM','SYMPREC','GGA','ISMEAR','SIGMA','KSPACING','KGAMMA','LREAL','NELM','NELMIN'))

def read_vasp(vasprun_stream, keep_param_tags = KEEP_PARAM_TAGS):
    """Read CfgCalc from vasp 5 OUTCAR
    """
    dd = xmltodict.parse(vasprun_stream.read())
    parse(dd)
    
    match = re.match(r'\s*((\d+)\.(\d+)\.(\d+))', dd['modeling']['generator']['version'])
    if(match):
        vasp_major_version = int(match.group(2))
        vasp_minor_version = int(match.group(3))
        vasp_micro_version = int(match.group(4))
    else:
        raise NotImplementedError('Error: unrecognized vasp version')

    ismear = dd['modeling']['parameters']['ISMEAR']

    calc_cfgs = []
    calcs = dd['modeling']['calculation']
    if not isinstance(calcs, list): calcs = [calcs]
    for calc in calcs:
        if(len(calc['scstep']) < dd['modeling']['parameters']['NELM']):
            cell = calc['structure']['crystal']['basis']
            pos = calc['structure']['positions']
            pos = np.dot(pos, cell)
            types = [e['element'] for e in dd['modeling']['atominfo']['atoms']]
            calc_cfg = CalcCfg(Cfg(cell = cell,
                pos = pos,
                types = types))
            calc_cfg.energy = calc['energy']['e_wo_entrp'] if ismear>=1 else calc['energy']['e_fr_energy']
            calc_cfg.forces = calc['forces']
            if 'stress' in calc and not (calc['stress'] is None or (isinstance(calc['stress'], np.ndarray) and (calc['stress'] == None).all())):
                calc_cfg.stress = calc['stress'] / 1602.176621 * calc['structure']['crystal']['volume']
            params = {k:v for k,v in dd['modeling']['parameters'].items() if k in keep_param_tags}
            if 'PREC' in params:
                params['PREC'] = params['PREC'][0]
            params['potcar_list'] = [el['pseudopotential'] for el in dd['modeling']['atominfo']['atomtypes']]
            calc_cfg.method = VaspPotential(params = params)
            calc_cfgs.append(calc_cfg)

    #CalcCfg.saved_dd = dd   # this is sometimes used for debugging

    return calc_cfgs if len(calc_cfgs) != 1 else calc_cfgs[0]

class GenericVasp(AnyJob):
    """Generic VASP calculation
    
    Usage: ::

      job = GenericLammps(cfg, incar_dict = {'ENCUT':300, 'KSPACING': 0.2}, potcar_list = ['PAW_PBE Al 04Jan2001'], extra_out_files = {'OSZICAR': str})

    Returns OUTCAR, stdout, and stdin, and everything in extra_out_files like a FileJob returns.
    One can pass an ``extra_in_files`` argument.
    """

    _is_safe_to_serialize = True

    def _vasp_run():
        from atomicasoft.jobs import job_info
        import atomicasoft.core.resources as resources
        if 'n_cores' not in job_info('metadata'):
            raise RuntimeError('run VASP with run_job type of command')
        n_cores = job_info('metadata')['n_cores']
        stdout, stderr = resources.vasp5_mpi.run('std', n_cores)
        return {'stdout':stdout, 'stderr':stderr}

    def __call__(self):
        def convert_param_val(v):
            if isinstance(v, bool):
                return '.TRUE.' if v else '.FALSE.'
            return str(v)
        incar = ''.join([f'{str(key)} = {convert_param_val(val)}\n' for key,val in self.incar_dict.items()])

        kpoints = ''
        if self.incar_dict.get('KSPACING') is None:
            if self.k_mesh is None: raise ValueError("k-point mesh is not set. Set either incar_dict['KSPACING'] or k_mesh")
            if isinstance(self.k_mesh, list) and len(self.k_mesh) == 3:
                # uniform gamma-centered mesh
                kpoints = f"""\
atomica_user_defined_uniform_mesh
 0
Gamma
 {' '.join(self.k_mesh)}
 0 0 0
"""
        if self.incar_dict.get('KSPACING') is None and not kpoints:
            raise ValueError("k-point mesh is wrongly set up or not implemented")

        # now: pseudopotentials
        potcar = ''
        if isinstance(self.potcar_list, str):
            self.potcar_list = [self.potcar_list]
        elems = []
        for p in self.potcar_list:
            if p.count('\n') <= 1:
                # look for this potcar
                elem_val_el = p.split()[1]
                path = resources.vasp5_mpi.pp_dir / elem_val_el / 'POTCAR'
                if not path.is_file():
                    raise ValueError(f'Pseudopotential file {path} not found')
                with open(path, 'r') as f:
                    pp = f.read()
                    l = pp.split('\n', 1)[0]
                    if not l.strip() == p:
                        raise ValueError(f"Pseudopotential is found in {path}, but it is '{l.strip()}' and not the requested '{p}'")
                    elems.append(elem_val_el)
                    potcar += pp
            else:
                potcar += p 

        elems = [re.match('[A-Za-z]*',e).group(0) for e in elems]
        poscar = atomicasoft.core.VaspPoscar(self.cfg, elems)

        in_files = {'INCAR':incar,
                    'POSCAR':poscar,
                    'POTCAR':potcar,
                    **self.extra_in_files}
        if kpoints:
            in_files['KPOINTS'] = kpoints
                    
        job = FileJob(GenericVasp._vasp_run, in_files = in_files,
                      out_files = {'vasprun.xml': str, **self.extra_out_files})
        ret = job()
        with open('_atomica_jobrouter_stdout', 'wb') as f:
            f.write(ret['stdout'])
        with open('_atomica_jobrouter_stderr', 'wb') as f:
            f.write(ret['stderr'])
        #calc_cfg = atomicasoft.core.calc_cfg.CalcCfg.read_vasp5_outcar('OUTCAR')
        return ret # {'calc_cfg':calc_cfg, 'out_files': ret}

    def __init__(self, cfg: Cfg, incar_dict = {}, k_mesh = None, potcar_list = None, extra_in_files = {}, extra_out_files = {}):
        self.metadata['needs_dir'] = True
        self.resources.add('vasp5_mpi')
        self.cfg = cfg
        self.incar_dict = incar_dict
        self.k_mesh = k_mesh
        self.potcar_list = potcar_list
        self.extra_in_files = extra_in_files
        self.extra_out_files = extra_out_files

class VaspPotential(AnyJob):
    """VaspPotential class for computing CalcCfg with VASP.

    :param params: A dictionary containing INCAR and POTCAR parameters.
                   INCAR parameters are given as tags, e.g., 'ENCUT', 'ISMEAR', etc
                   Must include 'potcar_list' to specify the list of POTCAR files,
                   e.g., 'potcar_list': ['PAW_PBE Al 04Jan2001']
    :type params: dict

    :param incar_tags: A set of INCAR tags to read back from the calculation.
                       Default is a predefined set of commonly used tags.
    :type incar_tags: set, optional

    Note:
    The 'needs_dir' metadata is set to True, and the 'vasp5_mpi' resource is appended
    to the resources list, indicating that this job requires a directory and uses the 'vasp5_mpi' resource.

    Example:
    Create a VaspPotential object with custom INCAR tags::

        params = {'ENCUT':300,
                  'KSPACING': 0.5,
                  'KGAMMA': True,
                  'ISMEAR': 1,
                  'SIGMA': 0.1,
                  'PREC': 'Accurate',
                  'ISYM': 0,
                  'NELM': 80,
                  'NELMIN': 3,
                  'EDIFF': 1e-7,
                  'NCORE': 4,
                  'potcar_list': ['PAW_PBE Al 04Jan2001'],
                 }
        method = atomicasoft.core.interfaces.vasp.VaspPotential(params = params)

    Run the calculation on a given configuration::

        cfg = atomicasoft.core.Cfg(...)
        calc_cfg = atomicasoft.core.calc_cfg.CalcCfg(cfg = cfg, method = method)
        calc_cfg = calc_cfg() # it will now have energy, forces, and stresses calculated

    """
    _INCAR_TAGS = set(('ENCUT', 'KSPACING', 'KGAMMA', 'ISMEAR', 'SIGMA', 'PREC', 'ISYM', 'NELM', 'NELMIN', 'EDIFF', 'NCORE', 'IVDW'))
    _INCAR_DEFAULTS = {'LWAVE': False, 'LCHARG': False, 'ISTART': 1, 'ICHARG': 1}
    _INCAR_PRECOMPUTE = {'KGAMMA': True, 'KSPACING': 1e9, 'LWAVE': True, 'LCHARG': True, 'IBRION': -1}
    _OTHER_VALID_PARAMS = {'potcar_list'}
    def __init__(self, params, *, precompute_on_gamma = True, incar_tags = _INCAR_TAGS):
        assert isinstance(params, dict), 'VaspPotential params should be a dictionary'
        self.params = params
        self.incar_tags = incar_tags
        self.precompute_on_gamma = precompute_on_gamma
        self.metadata['needs_dir'] =  True
        self.resources.add('vasp5_mpi')

    def calc_cfg(self, cfg: Cfg):
        assert isinstance(cfg, Cfg), "Parameter 'cfg' should be of type atomicasoft.core.Cfg"
        filtered_out_params = set(self.params.keys()) - self.incar_tags - self._OTHER_VALID_PARAMS
        if filtered_out_params:
            logger.warning(f'The following params will be filtered out: {filtered_out_params}. If you insist on adding it, use VaspPotential(..., incar_tags = {filtered_out_params})')
        incar = {k:v for k,v in self.params.items() if k in self.incar_tags}
        incar = {**self._INCAR_DEFAULTS, **incar}
        potcar_list = self.params['potcar_list']
        if self.precompute_on_gamma:
            precompute_incar = {**incar, **self._INCAR_PRECOMPUTE}
            job = GenericVasp(cfg, incar_dict = precompute_incar, potcar_list = potcar_list)
            job()
        job = GenericVasp(cfg, incar_dict = incar, potcar_list = potcar_list)
        ret = job()
        calc_cfg = read_vasp(io.StringIO(ret['vasprun.xml']))
        return calc_cfg
    calc_cfg.metadata = {'needs_dir': True}
    calc_cfg.resources = ['vasp5_mpi']

    def relax_cfg(self, cfg: Cfg, n_steps_max = 80, constraints = False, keep_only_last = True):
        assert isinstance(cfg, Cfg), "Parameter 'cfg' should be of type atomicasoft.core.Cfg"
        incar = {k:v for k,v in self.params.items() if k in self.incar_tags}
        incar = {**self._INCAR_DEFAULTS, **incar}

        # relaxation parameters
        incar['IBRION'] = 2
        incar['ISIF'] = 3 if not constraints else 2
        incar['NSW'] = n_steps_max

        potcar_list = self.params['potcar_list']
        
        # Ignore precompute for relax jobs
        #if self.precompute_on_gamma:
        #    precompute_incar = {**incar, **self._INCAR_PRECOMPUTE}
        #    job = GenericVasp(cfg, incar_dict = precompute_incar, potcar_list = potcar_list)
        #    job()
        
        job = GenericVasp(cfg, incar_dict = incar, potcar_list = potcar_list)
        ret = job()
        calc_cfg = read_vasp(io.StringIO(ret['vasprun.xml']))
        if keep_only_last:
             return calc_cfg[-1]
        return calc_cfg
    relax_cfg.metadata = {'needs_dir': True}
    relax_cfg.resources = ['vasp5_mpi']
