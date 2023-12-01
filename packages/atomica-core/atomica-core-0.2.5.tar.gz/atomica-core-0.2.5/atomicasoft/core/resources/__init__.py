"""Package managing user resources like LAMMPS or VASP

Imports resources. The resources are first imported from the user's resource folder
(by default located at ``~/.atomica/resources``) and then from the current folder and python path.
This allows the user to adjust the module code by copying the corresponding file
(like ``mlip2_mpi.py``) to ``~/.atomica/resources`` and make modifications there.

``import resources`` first looks for the files ``*.py``, imports all these files as modules
and runs ``test()`` in each of these modules. If ``test()`` returns ``True`` then
we add this module to modules variable. Thus, the code ::

  import resources
  print(resources.modules)

prints the list of all modules available on this machine.
"""

import pathlib as _pathlib
import re as _re

_NODE_RESOURCES_PATH = _pathlib.Path.home() / '.atomica' / 'resources'

# first import from user's resources
import sys as _sys
_sys.path.insert(1, _NODE_RESOURCES_PATH)

# creating the dictionary of modules
modules = {}

for _p in _pathlib.Path(_NODE_RESOURCES_PATH).glob('*.py'):
    if _p.name.startswith('__'): continue
    _name = _re.sub('\.py$','' , _p.name)
    exec(f'import {_name}')
    modules[_name] = _p

for _p in _pathlib.Path(__file__).parent.glob('*.py'):
    if _p.name.startswith('__'): continue
    _name = _re.sub('\.py$','' , _p.name)
    if(modules.get(_name) is None):
        exec(f'from . import {_name}')
        modules[_name] = _p

_module_names = list(modules.keys())

for _name in _module_names:
    if not eval(f'{_name}.test()'):
        del modules[_name]

del _name
del _module_names
