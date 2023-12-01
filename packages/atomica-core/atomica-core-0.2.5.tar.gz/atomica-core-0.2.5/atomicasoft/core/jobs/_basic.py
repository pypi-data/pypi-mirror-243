import copy

from atomicasoft.core.basic import Valerr
import atomicasoft.core, atomicasoft.core.hasher, atomicasoft.core.series, atomicasoft.core.calc_cfg
from . import _core

import atomicasoft.core.resources as resources

class CalcException(Exception):
    """A basic exception during job calculations, all exceptions that jobs raise
    as part of their normal functioning (e.g., ActiveLearning exceptions) should
    derive from this class
    """
    def __init__(self, message="Unhandled calculation exception: something went wrong"):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"CalcException: {self.message}"

class MultiCalcException(Exception):
    """An exception containing multiple exceptions.

    The `MultiCalcException` is effectively flat: normally `MultiCalcException`s
    do not contain other MultiCalcException objects
    """
    def __init__(self, exceptions=None):
        super().__init__()
        if exceptions is None:
            self.exceptions = []
        else:
            self.exceptions = exceptions

    def append(self, exception):
        if isinstance(exception, CalcException):
            self.exceptions.append(exception)
        else:
            raise TypeError("Only CalcException instances can be appended to MultiCalcException.")

    def __iadd__(self, multiexception):
        if isinstance(multiexception, MultiCalcException):
            self.exceptions += multiexception.exceptions
            return self
        else:
            raise TypeError("Only MultiCalcException instances can be added to MultiCalcException.")

    def __len__(self):
        return len(self.exceptions)
    
    def has_exceptions(self):
        return bool(self.exceptions)

    def __str__(self):
        if self.exceptions:
            messages = [str(exc) for exc in self.exceptions]
            return "MultiCalcException:\n" + "\n".join(messages)
        else:
            return "MultiCalcException: No exceptions added."

class ActiveLearningException(CalcException): 
    """An active learning exception. The field cfgs contains a configuration or a list of configurations
    that were selected for possible training.
    """
    def __init__(self, cfgs = None, message = 'Unhandled active learning exception'):
        super().__init__(message)
        self.cfgs = cfgs

class AnyJob:
    """An abstract job, defining common functionality like resource management or metadata
    """
    def __new__(cls, *args, **kwargs):
        # overriding constructor to create the metadata and resource fields
        self = object.__new__(cls)
        self.metadata = copy.copy(cls.metadata) if hasattr(cls, 'metadata') else {}
        self.resources = copy.copy(cls.resources) if hasattr(cls, 'resources') else set()
        return self
    pass

class FileJob(AnyJob):
    """Running a generic script, files as input, files as output

    Usage: ::

      def script():
          import subprocess
          ret = subprocess.run(['cp','a','c'])
          ret = subprocess.run(['cat','a','b'], capture_output = True)
          return {'stdout':ret.stdout, 'stderr':ret.stderr}
        
      job = FileJob(target = script, in_files = {'a': '123', 'b': 'abc'}, out_files = {'c': str})

    ``in_files`` can be of the form ``filename:True``, in which case it will be read from a local file.
    Alternatively, ``in_files`` can be ``[filename1, filename2, ...]`` --- all files will be read upon the job creation
    ``in_files`` can be of the form ``filename:atomicasoft.core.Hasher``, in which can it will be read from file and wrapped into ``Hasher()``.

    ``out_files`` is a dictionary ``{filename1: str, filename2: bytes}``, where str means it is a text file
    and bytes means it is a binary file. ``out_files`` can be a `list`, in which case they are interpreted as `bytes`

    Two extra parameters are args (default ()) and kwargs (default {})

    The job output will be a dictonary like ``{filename: contents}``.
    The script may write extra entires, like in the case above ``'stdout'`` and ``'stderr'``.
    """

    @staticmethod
    def _normalize_input_files(in_files) -> dict:
        # turns in_file to a dict
        if isinstance(in_files, str):
            in_files = {in_files: True}
        if isinstance(in_files, list):
            in_files = {fn: True for fn in in_files}
        if not isinstance(in_files, dict):
            raise TypeError('in_files should be list or dict')
        return in_files

    @staticmethod
    def _normalize_output_files(out_files) -> dict:
        # turns out_file to a dict
        if isinstance(out_files, list):
            out_files = {fn: bytes for fn in out_files}
        if not isinstance(out_files, dict):
            raise TypeError('out_files should be list or dict')
        for filename, t in out_files.items():
            if t is bytes or t == 'bytes':
                pass
            elif t is str or t == 'str':
                pass
            else: raise(TypeError(f'output file type should be str or bytes (but was {t})'))
        return out_files

    def __init__(self, target, args = (), kwargs = {}, *, in_files = {}, out_files = {}):
        self.metadata['needs_dir'] = True

        assert callable(target)
        self.target = target
        self.args = args
        self.kwargs = kwargs

        in_files = self._normalize_input_files(in_files)
        for fn in in_files:
            if in_files[fn] is True:
                with open(fn, 'rb') as f:
                    in_files[fn] = f.read()
            elif in_files[fn] is atomicasoft.core.Hasher:
                with open(fn, 'rb') as f:
                    in_files[fn] = atomicasoft.core.Hasher(f.read())
        for fn, val in in_files.items():
            val_type = type(val.data) if type(val) is atomicasoft.core.Hasher else type(val)
            if val_type is not str and val_type is not bytes:
                raise TypeError('in_files content should be str or bytes')
        self.in_files = in_files

        self.out_files = self._normalize_output_files(out_files)

    def __call__(self):
        import subprocess
        import time
        import os
    
        # input data
        for key, val in self.in_files.items():
            if isinstance(val, str):
                with open(key,"w") as f: f.write(val)
            elif isinstance(val, bytes):
                with open(key,"wb") as f: f.write(val)
            elif isinstance(val, atomicasoft.core.Hasher) and isinstance(val.data, str):
                with open(key,"w") as f: f.write(val.data)
            elif isinstance(val, atomicasoft.core.Hasher) and isinstance(val.data, bytes):
                with open(key,"wb") as f: f.write(val.data)

        out_dict = self.target(*self.args, **self.kwargs)
        if out_dict == None : out_dict = {} # note: "is None" is not pickling well
        assert type(out_dict) is dict
        
        for filename, t in self.out_files.items():
            try:
                if(t is bytes or t == 'bytes'):
                    with open(filename,"rb") as f:
                        out_dict[filename] = f.read()
                elif(t is str or t == 'str'):
                    with open(filename,"r") as f:
                        out_dict[filename] = f.read()
            except FileNotFoundError:
                out_dict[filename] = None
        return out_dict

class JobBundle(AnyJob):
    """A job that bundles multiple jobs together in an array.

    Usage: ::

      job = FileJob(job_array = [job_1, job_2, job_3])

    ``job_array`` is, unsurprisingly, an array of jobs. Each job is a tuple or list or dict
    as required by the ``run_job_array`` function.

    The job output will be an array of job outputs, equivalent to ``run_job_array(job_array)``.
    """

    def __init__(self, job_array):
        self.job_array = job_array

    def __call__(self):
        return _core.run_job_array(self.job_array)
