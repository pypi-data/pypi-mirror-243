"""Interface with the new MLIP package

"""

# import re, json, numpy as np, warnings, hashlib, string, random, io, pathlib

#from .. import ptable
from .. import cfg
from .. import calc_cfg
from .. import loss
#from ..basic import temp_file_path
#from .. import resources

import mlip

#from ..jobs._basic import *

def to_mlip_cfg(c: cfg.Cfg) -> mlip.Cfg:
    return mlip.Cfg(cell = c.cell, pos = c.pos, types = c.types)

def to_mlip_calc_cfg(c: calc_cfg.CalcCfg) -> mlip.CalcEfs:
    return mlip.CalcEfs(cfg = to_mlip_cfg(c.cfg), energy = c.energy, forces = c.forces, stress = c.stress.vector)

def to_mlip_loss_cfg(c: loss.LossCfg) -> mlip.CalcEfs:
    return mlip.LossEfs(sim = to_mlip_calc_cfg(c.calc_cfg), weight_energy = c.weight_energy, weight_forces = c.weight_forces, weight_stress = c.weight_stress)

def to_mlip_loss_function(loss_func: loss.LossFunction) -> mlip.CalcEfs:
    mlip_loss_func = mlip.LossFunction()
    for loss_term in loss_func.loss_term_list:
        assert type(loss_term) is loss.LossCfg, 'only LossCfg terms are implemented at the moment'
        mlip_loss_func.add(to_mlip_loss_cfg(loss_term))
    return mlip_loss_func
