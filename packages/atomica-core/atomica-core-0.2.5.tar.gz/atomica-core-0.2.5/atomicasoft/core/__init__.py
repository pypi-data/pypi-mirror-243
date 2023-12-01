"""
This is a package for basic manipulating atomistic modeling jobs.

To use the full power of this package, you need to set up resources
on the machine where you plan to perform calcualtions.
Resources are external (to this package) atomistic modeling tools.
Currently, three resources are supported: VASP (version 5), LAMMPS, and MLIP-2.

Typically, to set up a resource, you should create a ``.sh``-file
in the ``~/.atomica/resources/`` folder.
See what should be in this ``.sh``-file for
:py:mod:`LAMMPS<atomicasoft.core.resources.lammps_mpi>`,
:py:mod:`VASPv5<atomicasoft.core.resources.vasp5_mpi>`, and
:py:mod:`MLIP-2<atomicasoft.core.resources.mlip2_mpi>`.
"""

import pathlib as _pathlib
_NODE_RESOURCES_PATH = _pathlib.Path.home() / '.atomica' / 'resources'
_NODE_RESOURCES_PATH.mkdir(parents=True, exist_ok=True)

from . import ptable
from .basic import *
from .cfg import *

from . import hasher
from .hasher import Hasher

from .serialize import dumps, loads
