"""Package with functions handling jobs

Has functions like run_job. This package cannot be used by itself.
Instead, use `atm.core` or `atm.sched` to either run the jobs locally
or run the jobs through a server, respectively.

Typical usage:

>>> import atm.jobs
>>> import atm.core   # uncomment this line to run calculations locally
>>> # import atm.sched   # uncomment this line to run calculations through a server
>>> def my_add(l):
>>>     return sum(l)
>>>     
>>> my_add([2,3,4])
9
>>> atm.jobs.run_job(my_add, [2,3,4])
9

"""

from ._job_info_module import job_info

from ._core import *
