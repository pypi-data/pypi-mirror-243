import dill, pathlib, traceback, sys, os, subprocess, inspect

import atomicasoft.jobs
from atomicasoft.jobs import DebugTracebackException, _job_info_module
from .._utils import *

from . import _basic

from .._settings import config_core
node_settings = config_core.get('node', {})
NODE_JOBFILES_PATH = node_settings.get('jobfiles_path')
if NODE_JOBFILES_PATH:
    NODE_JOBFILES_PATH = pathlib.Path(NODE_JOBFILES_PATH)
    NODE_JOBFILES_PATH.mkdir(parents=True, exist_ok=True)

def script_from_file(atm_module_path = ''):
    return f"""\
#!{sys.executable}
import dill
import sys
sys.path.append(r'{str(atm_module_path)}')
from atomicasoft.core.jobs import run_jobdill
import atomicasoft.jobs._job_info_module

import atomicasoft.core

try:
    with open("_atomica_jobrouter_jobdill.pkl", "rb") as f:
        job_dill = f.read()
    with open("_atomica_jobrouter_metadata.pkl", "rb") as f:
        metadata = dill.load(f)

    job_dill, job_outcome = run_jobdill(job_dill, metadata)
    with open("_atomica_jobrouter_jobdill.pkl", "wb") as f:
        f.write(job_dill)
    with open("_atomica_jobrouter_joboutcome.pkl", "wb") as f:
        dill.dump(job_outcome, f)
except RuntimeError as err:
    print ('Error:', err)
"""

import secrets
import string

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string

def compose_job_path(job_id, node_jobfiles_path = NODE_JOBFILES_PATH):
    job_id = str(job_id)
    job_id.zfill(5)
    return node_jobfiles_path / ("job_" + job_id)

# this function may be called parallelly (e.g., in a separate thread)
def run_job_from_file(job_dill: bytes, metadata: dict):
    if 'job_id' in metadata:
        job_id = metadata['job_id']
    else:
        job_id = generate_random_string(25)
    job_path = compose_job_path(job_id)
    try:
        job_path.mkdir()
    except:
        job_dill = dill.dumps(f"Error: {job_path} could not be made (exists?)\n" + traceback.format_exc())
        job_outcome = {'failed': True}
        return job_dill, job_outcome

    try:
        with (job_path / "_atomica_jobrouter_jobdill.pkl").open("wb") as f:
            f.write(job_dill)
        with (job_path / "_atomica_jobrouter_metadata.pkl").open("wb") as f:
            f.write(dill.dumps(metadata))
    except:
        job_dill = dill.dumps(f"Error: job files could not be created")
        job_outcome = {'failed': True}
        return job_dill, job_outcome

    try:
        script = script_from_file(atm_module_path = pathlib.Path(__file__).parent.parent.parent.parent)
        with open(str(job_path / '_atomica_jobrouter_script.py'), "w", opener = secure_executable_opener) as f:
            f.write(script)
        job_output = subprocess.run([sys.executable, '_atomica_jobrouter_script.py'], cwd = str(job_path), capture_output=True) #, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        job_dill = dill.dumps("Error: job files written, but python cannot launch the job calculator.\n" + traceback.format_exc())
        job_outcome = {'failed': True}
        return job_dill, job_outcome

    try:
        with (job_path / "_atomica_jobrouter_jobdill.pkl").open("rb") as f:
            job_dill = f.read()
        with (job_path / "_atomica_jobrouter_joboutcome.pkl").open("rb") as f:
            job_outcome = dill.load(f)
        return job_dill, job_outcome

    except:
        job_dill = dill.dumps(f"Error: job ran, but outcome is not written to a file.\n\nJob output:\n{job_output.stdout.decode()}\nJob error log:\n{job_output.stderr.decode()}")
        job_outcome = {'failed': True}
        return job_dill, job_outcome

def run_jobdill(job_dill: bytes, metadata: dict):
    if metadata.get('needs_dir'):
        metadata['needs_dir'] = False
        return run_job_from_file(job_dill, metadata)

    try:
        job_dill = dill.loads(job_dill)
        if(type(job_dill) is not tuple): raise RuntimeError('job is not a tuple')
        if(inspect.isclass(job_dill[0])): return dill.dumps("job should be a callable object, not class (you should pass a class instance)"), {'failed': True}
        if(not callable(job_dill[0])): return dill.dumps("job is not callable"), {'failed': True}

        failed = False
        try:
            job_dill = run_job(job_dill[0], job_dill[1], job_dill[2], metadata = metadata)
        except Exception as exc:
            if metadata.get('debug'):
                raise exc
            failed = True
            job_dill = exc
        job_dill = dill.dumps(job_dill)
        job_outcome = {'failed': failed}
    except:
        job_dill = dill.dumps(traceback.format_exc())
        job_outcome = {'failed': True}
    return job_dill, job_outcome

def run_job(job_func, job_args = (), job_kwargs: dict = {}, metadata: dict = {}, resources: list = []):
    """Runs a job
    
    The job is described by ``job_func`` --- a function or another callable object
    (like a class with ``def __call__``), ``job_args`` --- a tuple of positional arguments,
    and ``job_kwargs`` --- a dictionary of keyword arguments.
    The job is executed as::
    
      return job_func(*job_args, **job_kwargs)

    job's ``metadata`` is a ``dict`` describing how the job should be handled
    and is filled with information at different stages.
    First, the user can specify some of the fields like ``metadata['n_cores_min'] = 16`` and
    ``metadata['n_cores_max'] = 36``. When the job is fetched from the server, it gets fields like
    ``metadata['job_id'] = 204513``. Then, when the job is scheduled to run on a compute code, it gets,
    e.g., ``metadata['n_cores'] = 20``.
    It can be used for the purposes of debugging.

    Note that ``job_func`` may itself has a field ``metadata``. In this case these values
    are used as default unless overriden by the user.

    job may be supplied together with a list of the needed ``resources`` --- it will be made sure
    that it runs only on a node with those resources.
    Like with ``metadata``, job_func itself may have a ``resources`` attribute.

    :param job_func: a function or object to be called
    :type job_func: callable object

    :param job_args: positional arguments for ``job_func``, defaults to ``()``
    :type job_args: tuple, optional

    :param job_kwargs: keyword arguments for ``job_func``, defaults to ``{}``
    :type job_kwargs: dict, optional

    :param metadata: metadata for the job, defaults to ``{}``
    :type metadata: dict, optional

    :param resources: list of resources for the job, defaults to ``[]``
    :type resources: list or set, optional

    :raises: DebugTracebackException when 'debug' is set to True in metadata, otherwise any exception that the job raises

    :return: job result
    """
    if(type(job_args) is not tuple): job_args = (job_args,)

    # job_func may have metadata
    if hasattr(job_func, 'metadata'):
        metadata = {**job_func.metadata, **metadata}

    if metadata.get('needs_dir'):
        metadata['needs_dir'] = False
        job_dill, job_outcome = run_job_from_file(dill.dumps( (job_func, job_args, job_kwargs) ), metadata)
        job_result = dill.loads(job_dill)
        is_failed = job_outcome['failed']
        if is_failed:
            if isinstance(job_result, str):
                raise DebugTracebackException(job_result)
            else:
                raise job_result
        return job_result
    n_cores = metadata.get('n_cores_min', 1) # 1 core if n_cores_min not set
    metadata.setdefault('n_cores', n_cores) # do not overwrite metadata['n_cores'] if set

    saved_metadata = _job_info_module.data.metadata
    _job_info_module.data.metadata = metadata
    try:
        ret = job_func(*job_args, **job_kwargs)
    except Exception as exc:
        if metadata.get('debug'):
            raise DebugTracebackException(traceback.format_exc())
        else: raise exc
        job_outcome = {'failed': True}
    _job_info_module.data.metadata = saved_metadata
    return ret
atomicasoft.jobs.run_job = run_job

def run_job_array(job_array, *, metadata: dict = {}, resources: list = []):
    """Run Multiple Jobs in an Array

    This function executes multiple jobs concurrently, allowing you to run a batch of
    job specifications provided in the `job_array`. Each job specification can be a callable
    object, a tuple, a list, or a dictionary.

    :param job_array: An array containing job specifications.
                      Each element of the array can be a callable object, a tuple, a list, or a dictionary.
                      If it is a tuple it is of the form ``(job_func, job_args, job_kwargs, job_metadata, job_resources)``.
                      If it is a dictionary then it is of the form
                      ``{'job_func': job_func,
                      'job_args': job_args,
                      'job_kwargs': job_kwargs,
                      'job_metadata': job_metadata,
                      'job_resources': job_resources}``
                      Some fields of the tuple or dictionary may be left out. 
    :type job_array: list

    :param metadata: Additional metadata for the jobs in the array.
                     This metadata takes precedence over any metadata provided within individual job specifications.
    :type metadata: dict, optional

    :param resources: Additional resources required for all jobs in the array.
                      These resources are combined with any resources specified within individual job specifications.
    :type resources: list, optional

    :return: A list containing the results of each executed job.

    :raises CalcException: If an exception occurs during the execution of a single job.
    :raises MultiCalcException: If exceptions occur during the execution of multiple jobs.
    """
    resources = set(resources)
    job_results = []
    calc_exceptions = _basic.MultiCalcException()
    for job_spec in job_array:
        if callable(job_spec): job_spec = (job_spec,)
        if isinstance(job_spec, (tuple, list)):
            job_func = job_spec[0]
            if len(job_spec) > 1: job_args = job_spec[1]
            else: job_args = ()
            if len(job_spec) > 2: job_kwargs = job_spec[2]
            else: job_kwargs = {}
            if len(job_spec) > 3: job_metadata = job_spec[3]
            else: job_metadata = {}
            if len(job_spec) > 4: job_resources = job_spec[4]
            else: job_resources = set()
        elif isinstance(job_spec, dict):
            job_func = job_spec['job_func']
            job_args = job_spec.get('job_args', ())
            job_kwargs = job_spec.get('job_kwargs', {})
            job_metadata = job_spec.get('metadata', {})
            job_resources = job_spec.get('resources', set())
        else: raise TypeError("elements of job_array should be callable objects, tuples, lists, or dicts")
        job_metadata = {**metadata, **job_metadata}
        job_resources = resources | job_resources
        try:
            job_results.append(run_job(job_func, job_args, job_kwargs, job_metadata, job_resources))
        except _basic.CalcException as exc:
            calc_exceptions.append(exc)
        except _basic.MultiCalcException as exc:
            calc_exceptions += exc

    if len(calc_exceptions) == 0: return job_results
    elif len(calc_exceptions) == 1: raise calc_exceptions.exceptions[0]
    else: raise calc_exceptions

atomicasoft.jobs.run_job_array = run_job_array