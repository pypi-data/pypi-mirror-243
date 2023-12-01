"""
***************
LAMMPS resource
***************

For resource to function, it requires
to have an executable ``lammps_run.sh`` in the resources folder.
``lammps_run.sh`` should run as

.. code-block:: shell

  $ lammps_run.sh n_cores <arguments-to-lammps>

Sample lammps_run.sh content:

.. code-block:: bash

  !/bin/bash
  
  module load Compiler/Intel/20u4
  mpirun -n $1 ~/.atomica/resources/bin/lammps_mpi ${@:2}

"""

import subprocess
import pathlib
import re

NODE_RESOURCES_PATH = pathlib.Path.home() / '.atomica' / 'resources'

def run(n_cores: int, script_filename: str, extra_params_list: list):
    ret = subprocess.run([str(pathlib.Path(NODE_RESOURCES_PATH) / 'lammps_run.sh'), str(n_cores), '-in', script_filename] + extra_params_list, capture_output=True)
    return ret.stdout, ret.stderr

def test():
    if not (pathlib.Path(NODE_RESOURCES_PATH) / 'lammps_run.sh').is_file(): return False
    return True
