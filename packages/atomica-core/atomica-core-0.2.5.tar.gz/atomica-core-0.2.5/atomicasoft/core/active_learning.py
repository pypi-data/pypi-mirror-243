# Authors: Alexander Shapeev, Danil Bortok, Irina Yarysheva, Ekaterina Spirande

"""
This module provides the implementation of an active learning strategy for potential energy surface exploration.
"""
import logging

import atomicasoft.jobs as jr
from .calc_cfg import CalcCfg
from .jobs import ActiveLearningException, MultiCalcException

logger = logging.getLogger(__name__)

class ActiveLearning:
    """
    An active learning class for exploring potential energy surfaces through iterations of training and selection.
    """
    def __init__(self,
                 pot = None,
                 train_set = None, 
                 qm_pot = None,
                 simulations = None,
                 trainer = None,
                 selector = None,
                 max_iter = 1000,
                 smart_hashing = True):
        """
        Initializes an ActiveLearning object.

        :param pot: The potential energy surface (PES) model.
        :type pot: object, optional

        :param train_set: The initial training set of configurations.
        :type train_set: list, optional

        :param qm_pot: The quantum mechanical potential used for calculating configurations.
        :type qm_pot: object, optional

        :param simulations: The list of simulations for which configurations are to be explored.
        :type simulations: list, optional

        :param trainer: The trainer object responsible for updating the potential energy surface model.
        :type trainer: object, optional

        :param selector: The selector object responsible for selecting configurations for DFT calculations.
        :type selector: object, optional

        :param max_iter: The maximum number of iterations for the active learning process. Default is 1000.
        :type max_iter: int, optional

        :param smart_hashing: Flag indicating whether smart hashing is enabled. Default is True.
        :type smart_hashing: bool, optional

        :return: An instance of the ActiveLearning class.
        :rtype: ActiveLearning
        """
        self.pot = pot
        self.train_set = train_set
        self.qm_pot = qm_pot
        self.simulations = simulations
        self.trainer = trainer
        self.selector = selector
        self.max_iter = max_iter
        self.smart_hashing = smart_hashing

    def __call__(self,
                 pot = None,
                 train_set = None, 
                 qm_pot = None,
                 simulations = None,
                 trainer = None,
                 selector = None,
                 max_iter = None,
                 smart_hashing = None):
        """
        Runs the active learning iterations.

        :param pot: The potential energy surface (PES) model.
        :type pot: object, optional

        :param train_set: The initial training set of configurations.
        :type train_set: list, optional

        :param qm_pot: The quantum mechanical potential used for calculating configurations.
        :type qm_pot: object, optional

        :param simulations: The list of simulations for which configurations are to be explored.
        :type simulations: list, optional

        :param trainer: The trainer object responsible for updating the potential energy surface model.
        :type trainer: object, optional

        :param selector: The selector object responsible for selecting configurations for DFT calculations.
        :type selector: object, optional

        :param max_iter: The maximum number of iterations for the active learning process. Default is 1000.
        :type max_iter: int, optional

        :param smart_hashing: Flag indicating whether smart hashing is enabled. Default is True.
        :type smart_hashing: bool, optional

        :return: An instance of the ActiveLearning class after the active learning loop.
        :rtype: ActiveLearning
        """
        if pot is not None: self.pot = pot
        if train_set is not None: self.train_set = train_set
        if qm_pot is not None: self.qm_pot = qm_pot
        if simulations is not None: self.simulations = simulations
        if trainer is not None: self.trainer = trainer
        if selector is not None: self.selector = selector
        if max_iter is not None: self.max_iter = max_iter
        if smart_hashing is not None: self.smart_hashing = smart_hashing

        from atomicasoft.core import Hasher

        for iter in range(self.max_iter):
            pot = Hasher(self.pot) if self.smart_hashing else self.pot
            job_array = [(sim, pot) for sim in self.simulations]
            try:
                cfgs = []
                sim_results = jr.run_job_array(job_array)
            except ActiveLearningException as al_exception:
                cfgs = al_exception.cfgs
                if not isinstance(cfgs, list):
                    cfgs = [cfgs]
            except MultiCalcException as multi_exception:
                for exc in multi_exception.exceptions:
                    assert isinstance(exc, ActiveLearningException)
                    new_cfgs = exc.cfgs
                    if not isinstance(new_cfgs, list):
                        new_cfgs = [new_cfgs]
                    cfgs += new_cfgs

            # the configurations for active learning are in the cfgs list
            # if it is empty then we are done
            if not cfgs:
                logger.info('Loop done')
                break

            # select-add step
            selected_cfgs = jr.run_job(self.selector,
                                       job_kwargs = {'pot': pot,
                                                     'train_set': self.train_set,
                                                     'extrapolative_cfgs': cfgs})
            if type(selected_cfgs) is not list:
                selected_cfgs = [selected_cfgs]

            logger.info(f'Selected {len(selected_cfgs)} configurations for DFT calculations')
                
            # calculate the collected cfgs:
            calc_cfgs_jobs = [(CalcCfg(cfg = c.cfg, method = self.qm_pot),) for c in selected_cfgs]
            calc_cfgs = jr.run_job_array(calc_cfgs_jobs)
            
            # some CalcCfg jobs might not converge, in which case remove that configuration
            calc_cfgs = [c for c in calc_cfgs if type(c) is CalcCfg]
            
            self.train_set += calc_cfgs
            calc_cfgs = None

            # train
            self.pot = jr.run_job(self.trainer,
                                  job_kwargs = {'pot': self.pot,
                                                'train_set': self.train_set})
            logger.info(f'Iteration done; new train set size: {len(self.train_set)}')
            
        return self
        
    def __repr__(self):
        return f'<ActiveLearning object, pot={self.pot}, qm_pot={self.qm_pot}, {len(self.simulations)} simulation(s)>'
    