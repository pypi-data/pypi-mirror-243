"""
*******************************************
Vasp version 5 resource (tested with 5.4.4)
*******************************************

Requires to have an executable ``vasp5_run.sh`` in the resources folder
and the other/vasp_pp/ folder with the potentials. The contents of the 
other/vasp_pp/ folder should be like

  other/vasp_pp/Ac/POTCAR
  other/vasp_pp/Ag/POTCAR
  other/vasp_pp/Ag_GW/POTCAR
  ...

``vasp5_run.sh`` should run as

.. code-block:: shell

  $ vasp_run.sh std n_cores

``std`` can be changed to ``gam`` or ``ncl``.

Sample vasp5_run.sh content:

.. code-block:: bash

  !/bin/bash
  
  module load Compiler/Intel/20u4
  mpirun -n $2 ~/.atomica/resources/bin/vasp_$1 ${@:3}
"""

import subprocess
import pathlib
import re

NODE_RESOURCES_PATH = pathlib.Path.home() / '.atomica' / 'resources'

def run(exe_type: str, n_cores: int, extra_params_list: list = []):
    ret = subprocess.run([str(pathlib.Path(NODE_RESOURCES_PATH) / 'vasp5_run.sh'), exe_type, str(n_cores)] + extra_params_list, capture_output=True)
    return ret.stdout, ret.stderr

pp_dir = pathlib.Path(NODE_RESOURCES_PATH) / 'other' / 'vasp_pp'

def test():
    #try:
    #    stdout, stderr = run('std', 1)
    #except FileNotFoundError:
    #    return False
    if not (pathlib.Path(NODE_RESOURCES_PATH) / 'vasp5_run.sh').is_file(): return False
    if not pp_dir.is_dir(): return False
    return True
