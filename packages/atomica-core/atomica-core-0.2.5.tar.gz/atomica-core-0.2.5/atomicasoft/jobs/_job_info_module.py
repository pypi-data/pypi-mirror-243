class JobInfo:
    pass
data = JobInfo()
data.metadata = {} # by default run on one core
# data.metadata = {'n_cores': 1} # by default run on one core

def job_info(key: str):
    """A function returning job information (for now, only metadata).

    Typical usage: ::

      def run_vasp():
          n_cores = atm.jobs.job_info('metadata')['n_cores']
          vasp_params['NCORE'] = int(np.sqrt(n_cores))
          ...

    :param key: name of the job_info parameter (for now, only 'metadata')
    :type key: str

    :return: parameter (metadata dictionary)

    """
    return getattr(data, key)
