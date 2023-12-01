"""Defines `class` ``LossCfg`` used for training MLIPs

"""

import numpy as np

from . import ptable
from . import cfg as _cfg
from . import calc_cfg as _calc_cfg

class LossCfg:
    """Class describing a loss term with CalcCfg
    """

    _is_safe_to_serialize = True

    def _expanded_weight_stress(self):
        weight_stress = self.weight_stress
        if isinstance(weight_stress, (int, float, complex, np.number)):
            weight_stress = np.repeat(float(weight_stress), 6)
        elif len(weight_stress) == 6:
            weight_stress = np.array(weight_stress, dtype = float)
        elif len(weight_stress) == 3 and len(weight_stress[0]) == 3 and len(weight_stress[1]) == 3 and len(weight_stress[2]) == 3:
            weight_stress = np.array([weight_stress[0][0],weight_stress[1][1],weight_stress[2][2],
                                      (weight_stress[1][2]+weight_stress[2][1]),
                                      (weight_stress[0][2]+weight_stress[2][0]),
                                      (weight_stress[0][1]+weight_stress[1][0])], dtype = float)
        else:
            raise ValueError("Invalid weight_stress")
        return weight_stress

    def _expanded_weight_forces(self):
        weight_forces = self.weight_forces
        n_atoms = self.calc_cfg.cfg.n_atoms
        if isinstance(weight_forces, (int, float, complex, np.number)):
            weight_forces = np.repeat(float(weight_forces), n_atoms * 3).reshape(n_atoms, 3)
        elif len(weight_forces) == n_atoms and isinstance(weight_forces[0], (int, float, complex, np.number)):
            weight_forces = np.repeat(np.array(weight_forces, dtype = float), 3).reshape(n_atoms, 3)
        elif len(weight_forces) == n_atoms and len(weight_forces[0]) == 3:
            weight_forces = np.repeat(np.array(weight_forces, dtype = float), 3).reshape(n_atoms, 3)
        else:
            raise ValueError("Invalid weight_forces")
        return weight_forces

    def __init__(self, calc_cfg, *,
                 weight_energy = None,
                 weight_forces = None,
                 weight_stress = None):
        self.calc_cfg = calc_cfg
        if weight_energy is None:
            weight_energy = 1.0
        if weight_forces is None:
            weight_forces = 0.01
        if weight_stress is None:
            weight_stress = 0.001
        self.weight_energy = weight_energy
        self.weight_forces = weight_forces
        self.weight_stress = weight_stress
        self._expanded_weight_forces() # return value ignored - checking if it raises an exception
        self._expanded_weight_stress() # return value ignored - checking if it raises an exception

    def __repr__(self):
        return (f'LossCfg({format(self.calc_cfg)}'
                f', weight_energy = {self.weight_energy}'
                f', weight_forces = {self.weight_forces}'
                f', weight_stress = {self.weight_stress})')

class LossFunction:
    def __init__(self, loss_term_list: list = []):
        self.loss_term_list = loss_term_list
    def __repr__(self):
        return f'<LossFunction object, {len(self.loss_term_list)} terms>'
