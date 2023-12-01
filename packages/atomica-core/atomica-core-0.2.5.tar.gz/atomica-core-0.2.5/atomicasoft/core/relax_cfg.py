"""Defines `class` ``RelaxCfg``

"""

import numpy as np, copy, re, pathlib

import atomicasoft.jobs as jr

from . import ptable
from . import cfg

class RelaxCfg:
    """Class describing a ''configuration relaxation''
    """

    _is_safe_to_serialize = True

    def __init__(self, cfg, *, method = None, constraints = False, keep_only_last = True):
        self.cfg = cfg
        if method: self.method = method
        self.constraints = constraints
        self.keep_only_last = keep_only_last

    @property
    def metadata(self):
        ret = {}
        if hasattr(self, 'method'):
            if hasattr(self.method, 'metadata'):
                ret = {**ret, **self.method.metadata}
            if hasattr(self.method, 'relax_cfg') and hasattr(self.method.relax_cfg, 'metadata'):
                ret = {**ret, **self.method.relax_cfg.metadata}
        return ret

    @property
    def resources(self):
        ret = set()
        if hasattr(self, 'method'):
            if hasattr(self.method, 'resources'):
                ret.update(self.method.resources)
            if hasattr(self.method, 'relax_cfg') and hasattr(self.method.relax_cfg, 'resources'):
                ret.update(self.method.relax_cfg.resources)
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
        if hasattr(self,'method'): s += f', method = {self.method}'
        return f'RelaxCfg(cfg = {format(self.cfg)}{s})'

    def __call__(self):
        if not hasattr(self, 'method'):
            raise AttributeError('RelaxCfg object needs the method attribute to run a simulation')
        if not hasattr(self.method, 'relax_cfg'):
            raise AttributeError('Method does not have the relax_cfg attribute')
        if not callable(self.method.relax_cfg):
            raise AttributeError('Method attribute relax_cfg is not callable')
        return self.method.relax_cfg(self.cfg,
                                     constraints = self.constraints,
                                     keep_only_last = self.keep_only_last)
