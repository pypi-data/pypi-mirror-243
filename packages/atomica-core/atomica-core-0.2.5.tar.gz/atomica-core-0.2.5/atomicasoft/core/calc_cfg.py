"""Defines `class` ``CalcCfg``

"""

import numpy as np, copy, re, pathlib
#warnings
#import pymatgen.io.vasp

import atomicasoft.jobs as jr

from . import ptable
from . import cfg

class Stress:
    """
    Represents a six-component stress tensor.

    This class provides methods to access and manipulate the stress components
    stored as a 6-long stress vector. It also offers properties to retrieve the
    stress matrix and the principal stresses.

    :param stress: A 6-long vector or a 3x3 matrix, can be lists or np.array
    :type stress: list or numpy.ndarray

    :raises ValueError: If the input stress is not a stress in a valid format.

    :ivar vector: The stress vector as a 6-long list.
    :vartype vector: numpy.ndarray

    :return: None
    
    :Usage Example:
        stress = Stress([10, 20, 30, 40, 50, 60])
        print(stress)  # Output: Stress([10.0, 20.0, 30.0, 40.0, 50.0, 60.0])
        print(stress.vector)  # Output: [10. 20. 30. 40. 50. 60.]
        print(stress.matrix)
        stress.vector = [70, 80, 90, 100, 110, 120]
        print(stress.vector)  # Output: [ 70.  80.  90. 100. 110. 120.]
        stress.matrix = [[1,6,5],[6,2,4],[5,4,3]]
        print(stress) # Output: Stress([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        stress_copy = Stress(stress) # one can initialize Stress with another instance
        stress_copy.vector = stress # or assign another instance
    """

    @property
    def vector(self):
        return self._vector

    @vector.setter
    def vector(self, stress):
        if isinstance(stress, Stress):
            self._vector = stress._vector
        elif len(stress) == 6:
            self._vector = np.array(stress, dtype = float)
        elif len(stress) == 3 and len(stress[0]) == 3 and len(stress[1]) == 3 and len(stress[2]) == 3:
            self._vector = np.array([stress[0][0],stress[1][1],stress[2][2],
                                     0.5 * (stress[1][2]+stress[2][1]),
                                     0.5 * (stress[0][2]+stress[2][0]),
                                     0.5 * (stress[0][1]+stress[1][0])], dtype = float)
        else:
            raise ValueError("Invalid input. Expected a 6-long vector or a 3x3 matrix or a Stress instance.")

    def __init__(self, stress):
        self.vector = stress
        
    @property
    def matrix(self):
        matrix = np.array([
            [self._vector[0], self._vector[3], self._vector[4]],
            [self._vector[3], self._vector[1], self._vector[5]],
            [self._vector[4], self._vector[5], self._vector[2]]
        ])
        return matrix

    @matrix.setter
    def matrix(self, stress):
        if len(stress) == 3 and len(stress[0]) == 3 and len(stress[1]) == 3 and len(stress[2]) == 3:
            self._vector = np.array([stress[0][0],stress[1][1],stress[2][2],
                                     0.5 * (stress[1][2]+stress[2][1]),
                                     0.5 * (stress[0][2]+stress[2][0]),
                                     0.5 * (stress[0][1]+stress[1][0])], dtype = float)
        else:
            raise ValueError("Invalid input. Expected a 3x3 matrix.")

    def __eq__(self, other):
        return (self._vector == other._vector).all()
    def __repr__(self):
        return f"Stress({self._vector.tolist()})"

class CalcCfg:
    """Class describing a ''configuration calculation''
    """

    _is_safe_to_serialize = True

    def __init__(self, cfg, *, energy = None, forces = None, stress = None, method = None):
        self.cfg = cfg
        if energy: self.energy = energy
        if forces: self._forces = np.array(forces)
        if stress: self._stress = Stress(stress)
        if method: self.method = method

    @property
    def stress(self):
        return self._stress

    @stress.setter
    def stress(self, new_stress):
        self._stress = Stress(new_stress)

    @property
    def forces(self):
        return self._forces

    @forces.setter
    def forces(self, new_forces):
        self._forces = np.array(new_forces)

    @property
    def metadata(self):
        ret = {}
        if hasattr(self, 'method'):
            if hasattr(self.method, 'metadata'):
                ret = {**ret, **self.method.metadata}
            if hasattr(self.method, 'calc_cfg') and hasattr(self.method.calc_cfg, 'metadata'):
                ret = {**ret, **self.method.calc_cfg.metadata}
        return ret

    @property
    def resources(self):
        ret = set()
        if hasattr(self, 'method'):
            if hasattr(self.method, 'resources'):
                ret.update(self.method.resources)
            if hasattr(self.method, 'calc_cfg') and hasattr(self.method.calc_cfg, 'resources'):
                ret.update(self.method.calc_cfg.resources)
        return ret

    def __eq__(self, other) -> bool:
        if self.cfg != other.cfg: return False
        if set(self.__dict__.keys()) != set(other.__dict__.keys()):
            return False
        for f in self.__dict__:
            if isinstance(self.__dict__[f], np.ndarray):
                if not (self.__dict__[f]==other.__dict__[f]).all():
                    return False
            else:
                if self.__dict__[f] != other.__dict__[f]:
                    return False
            
        return True

    def __repr__(self):
        s = ''
        if hasattr(self,'energy'): s += f', energy = {self.energy}'
        if hasattr(self,'forces'): s += f', forces = {format(self.forces.tolist())}'
        if hasattr(self,'stress'): s += f', stress = {format(self.stress.vector.tolist())}'
        if hasattr(self,'method'): s += f', method = {self.method}'
        return f'CalcCfg(cfg = {format(self.cfg)}{s})'

    def __call__(self):
        if not hasattr(self, 'method'):
            raise AttributeError('CalcCfg object needs the method attribute to run a simulation')
        if not hasattr(self.method, 'calc_cfg'):
            raise AttributeError('Method does not have the calc_cfg attribute')
        if not callable(self.method.calc_cfg):
            raise AttributeError('Method attribute calc_cfg is not callable')
        return self.method.calc_cfg(self.cfg)
