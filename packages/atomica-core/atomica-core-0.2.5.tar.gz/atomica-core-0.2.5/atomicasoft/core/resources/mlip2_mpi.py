"""
***************
MLIP-2 resource
***************

MLIP-2 is a software package for Machine Learning Interatomic Potentials
available at https://gitlab.com/ashapeev/mlip-2.
This module establishes an interface between this pyton package and the MLIP-2 binary.

Requires to have an executable ``mlp_run.sh`` in the resources folder.
``mlp_run.sh`` should run as

.. code-block:: shell

  $ mlp_run.sh n_cores <arguments-to-mlip>

For example

.. code-block:: shell

  $ mlp_run.sh 40 train pot.mtp train.cfg

Sample mlp_run.sh content (modify it according to your environment):

.. code-block:: bash

  !/bin/bash
  
  module load Compiler/Intel/20u4
  mpirun -n $1 ~/.atomica/resources/bin/mlp_mpi ${@:2}
"""

import subprocess
import pathlib
import re

NODE_RESOURCES_PATH = pathlib.Path.home() / '.atomica' / 'resources'

_exe_path_candidates = [pathlib.Path(NODE_RESOURCES_PATH) / 'mlp_run.sh',
                        pathlib.Path(NODE_RESOURCES_PATH) / 'mlp_run.bat']
exe_path = None

def run(n_cores: int, params_list: list = []):
    ret = subprocess.run([exe_path, str(n_cores)] + params_list, capture_output=True)
    return ret.stdout, ret.stderr

def test():
    global exe_path
    for p in _exe_path_candidates:
        if p.is_file():
            exe_path = str(p)
            return True
    return False
