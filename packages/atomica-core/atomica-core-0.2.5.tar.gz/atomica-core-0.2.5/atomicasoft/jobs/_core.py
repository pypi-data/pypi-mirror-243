class DebugTracebackException(Exception):
    """This exception is thrown when trying to get the result of the the job
    that did not run correctly.
    """
    pass

def run_job(*args, **kwards):
    """Placeholder for running a job

    Overwritten with ``import atm.core`` or ``import atm.sched``.
    """
    raise NotImplementedError("You should `import atm.core` to get this function to work.")

def run_job_array(job_array, *, metadata: dict = {}, resources: list = []):
    """Placeholder for running an array of jobs

    Overwritten with ``import atm.core`` or ``import atm.sched``.
    """
    raise NotImplementedError("You should `import atm.core` to get this function to work.")
