"""Slurm scheduler

Provides the Slurm adaptor class
"""

import subprocess, re, getpass, pathlib

USERNAME = getpass.getuser()

class Slurm:
    """A Slurm adaptor class.

    Provides the following operations:
    - get_nodelist(): retrieve a list of nodes avaible for slurm
    - get_jobs(): retrievea list of user's jobs currently running
    - submit(): submit a job
    - cancel_jobs(): cancel one or more jobs

    These operations are done by system calls to `squeue`, `sbatch`, etc.
    """
    STATUS_TRANSLATION = {'RUNNING': 'running',
                          'PENDING': 'pending',
                          'COMPLETING': 'completing'}
    
    def __init__(self):
        pass

    def timestring_to_seconds(self, timestring: str) -> int:
        """
        Convert a timestring that slurm prints out to the number of seconds
        """
        time_formats = [f"^(\d*)-(\d*):(\d*):(\d*)$", f"^(\d*):(\d*):(\d*)$", f"^(\d*):(\d*)$", f"^(\d*)$"]
    
        if(timestring == 'infinite'):
            seconds = None
        else:
            matches = [re.match(f, timestring) for f in time_formats]
            seconds = sum([int(a)*[1,60,3600,3600*24][i] for i,a in enumerate(list(reversed([m.groups() for m in matches if m is not None][0])))])
        return seconds
    
    def seconds_to_timestring(self, seconds: int) -> str:
        """
        Convert a number of seconds to the timestring recognizable by the slurm
        """
        if(seconds is None): return '00:00:00'
        seconds = int(seconds)
        timestring = '{:0>2}'.format(seconds % 60)
        seconds = seconds // 60
        timestring = ('{:0>2}'.format(seconds % 60)) + ':' + timestring
        seconds = seconds // 60
        timestring = ('{:0>2}'.format(seconds % 24)) + ':' + timestring
        seconds = seconds // 24
        if(seconds == 0): return timestring
        return f"{seconds}-" + timestring
    
    def _from_slurm_status(s: str) -> str:
        if(s in Slurm.STATUS_TRANSLATION): s = Slurm.STATUS_TRANSLATION[s]
        return s
    
    def get_nodelist(self):
        """Retrieve a list of compute nodes from the Slurm sinfo command.

        This method runs the 'sinfo' command, processes its output, and returns a list
        of compute nodes with relevant information.

        Returns:
            list: A list of dictionaries, each containing information about a compute node.

        Each dictionary includes the following fields:
        - 'partition': The partition to which the node belongs.
        - 'n_cores': The total number of CPU cores on the node.
        - 'n_cores_avail': The number of currently available CPU cores on the node. Equals to 'n_cores' if the node is not occupied.
        - 'memory': The total memory on the node (in megabytes).
        - 'memory_avail': The available memory on the node (in megabytes).
        - 'timelimit': The maximum time limit for jobs on the node (in seconds). None if there is no time limit.
        - 'name': The name of the node.

        Example:
        ::
            [
                {
                    'partition': 'compute',
                    'n_cores': 16,
                    'n_cores_avail': 8,
                    'memory': 65536,
                    'memory_avail': 32768,
                    'timelimit': None,
                    'name': 'node1'
                },
                {
                    'partition': 'gpu',
                    'n_cores': 8,
                    'n_cores_avail': 8,
                    'memory': 32768,
                    'memory_avail': 32768,
                    'timelimit': 7200,
                    'name': 'node2'
                },
                # More nodes...
            ]
        """
        result = subprocess.run(['sinfo', '-o', '%all'], stdout=subprocess.PIPE)
        result = result.stdout.decode()
        result = result.splitlines()
        keys = [s.strip() for s in result[0].split('|')]
        nodes = [dict(zip(keys,[s.strip() for s in res.split('|')])) for res in result[1:]]
        
        nodelist = []
        
        for n in nodes:
            name = n['HOSTNAMES']
            partition = n['PARTITION'].replace('*','')
            cpus = int(n['CPUS'])
            cpus_idle = int(n['CPUS(A/I/O/T)'].split('/')[1])
            memory = int(n['MEMORY'])
            memory_avail = int(n['FREE_MEM'])
            seconds = self.timestring_to_seconds(n['TIMELIMIT'])
            nodelist.append({'partition': partition, 'n_cores': cpus, 'n_cores_avail': cpus_idle, 'memory': memory, 'memory_avail': memory_avail, 'timelimit': seconds, 'name': name})
            timestring = self.seconds_to_timestring(seconds)
    
        return nodelist
    
    def get_jobs(self):
        """
        Retrieve a list of currently running jobs from the Slurm scheduler.

        This method runs the 'squeue' command to obtain information about running jobs.
        It parses the output and returns a list of dictionaries, each representing a running job.
        
        Returns:
            list: A list of dictionaries, each containing information about a running job.
            
        Each dictionary includes the following fields:
        - 'job_id' (int): The unique identifier for the job.
        - 'status' (str): The current status of the job, represented as a human-readable string.

        Example:
        ::
            [
                {'job_id': 12345, 'status': 'running'},
                {'job_id': 67890, 'status': 'pending'},
                # More job entries...
            ]
        """
        result = subprocess.run(['squeue', '-o', '%all', '-u', USERNAME], stdout=subprocess.PIPE)
        result = result.stdout.decode()
        result = result.splitlines()
        keys = [s.strip() for s in result[0].split('|')]
        jobs = [dict(zip(keys,[s.strip() for s in res.split('|')])) for res in result[1:]]
        jobs = [{'job_id':int(j['JOBID']), 'status': Slurm._from_slurm_status(j['STATE'])} for j in jobs] # if j['STATE'] == 'RUNNING']
        return jobs
    
    def cancel_jobs(self, slurm_ids):
        """
        Cancel one or more Slurm jobs by their unique job IDs.

        This method cancels Slurm jobs based on their unique job IDs provided as a list.
        
        Args:
            slurm_ids (int or list of int): The unique job ID(s) of the job(s) to be canceled.

        Example:
        ::
            # Cancel a single job by its job ID
            cancel_jobs(12345)

            # Cancel multiple jobs by their job IDs
            cancel_jobs([12345, 67890, 54321])
        """
        if(type(slurm_ids) is int): slurm_ids = [slurm_ids]
        if not slurm_ids: return 
        subprocess.run(['scancel'] + [f"{j}" for j in slurm_ids])#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def submit(self, *, job_path = None, script = None, script_name = None, job_name = None, partition = None, n_nodes:int = 1, n_cores:int = 1, memory = 1000, timelimit = None):
        """
        Submit a job to the Slurm scheduler.

        This method allows you to submit a job to the Slurm scheduler by specifying various parameters.
        You can provide either the job script as a multiline string that contains commands to run or
        the path to the script file (but not both). You can also specify the job path, job name, partition,
        number of nodes, number of CPU cores, memory, and time limit.

        Args:
            job_path (str or pathlib.Path, optional): The path where to run the script
            script (str, optional): The job script as a string.
            script_name (str, optional): The name of the job script file as a multiline string that contains commands to run.
            job_name (str, optional): The name to assign to the job.
            partition (str, optional): The Slurm partition to use for the job.
            n_nodes (int, optional): The number of nodes to allocate for the job.
            n_cores (int, optional): The number of CPU cores to allocate for the job.
            memory (int, optional): The amount of memory to allocate for the job (in megabytes).
            timelimit (int, optional): The maximum execution time for the job in seconds.

        Returns:
            int: The job ID assigned by Slurm.

        Raises:
            RuntimeError: If an error occurs during job submission.

        Example:
        ::
            # Submit a job with a script provided as a string
            script_text = f'''#!/bin/bash
            ~/scripts/mlp train {pot_file_name} ...
            '''
            job_id = submit(script=script_text, n_nodes=4, n_cores=96)

            # Submit a job with a script provided as a file path
            job_id = submit(script_name="/path/to/script/directory/my_script.sh",
                            job_path="/path/where/to/run/the/job",
                            n_nodes=1, n_cores=8, memory=2048, timelimit=3600)
        """
        assert script is not None or script_name is not None
        assert script is None or script_name is None

        if isinstance(job_path, pathlib.Path):
            job_path = str(job_path)

        sbatch_params = []
        if(partition is not None): sbatch_params += ["-p", partition]
        if(job_name is not None): sbatch_params += ["-J", job_name]
        sbatch_params += ["-N", f"{n_nodes}"]
        sbatch_params += ["-n", f"{n_cores}"]
        sbatch_params += ["--mem", f"{memory}"]
        sbatch_params += ["-t", self.seconds_to_timestring(timelimit)]

        if script_name is not None:
            result = subprocess.run(['sbatch'] + sbatch_params + [script_name], cwd = job_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                raise RuntimeError(f'Error running slurm script file {script_name}')
        else:
            if isinstance(script, str): script = script.encode()
            result = subprocess.run(['sbatch'] + sbatch_params, input = script, cwd = job_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                raise RuntimeError(f'Error running slurm script {script}')
        result = result.stdout.decode()
        return int(re.search("\d+", result).group())
