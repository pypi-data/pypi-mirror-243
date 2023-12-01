"""Time series management

"""
import numpy as np
#from statsmodels.tsa.ar_model import AutoReg
from typing import List, Union
from .basic import Valerr

# here self.size is the actual size of data
# self._data is a container than may have more entires than self.size
# use self.data for the actual data 
class TimeSeries:
    _is_safe_to_serialize = True

    def __init__(self, n_fields):
        self.n_fields = n_fields
        self._data = np.zeros((10, n_fields))
        self.length = 0
        self._stat = np.zeros((5, n_fields)) # sum(x_i), sum(x_i^2), sum(x_i x_{i+1}), min(x_i), max(x_i)

    def _realloc(self, new_size):
        new_size = max(int(len(self._data) * 1.125), new_size)
        old_data = self._data
        self._data = np.zeros( (new_size, self.n_fields) )
        self._data[:len(old_data),:] = old_data

    @property
    def data(self):
        return self._data[:self.length]

    def __len__(self):
        return self.length

    # adding list of lists
    def __iadd__(self, more_data):
        if len(self._data) < self.length + len(more_data):
            self._realloc(self.length + len(more_data))
        self._data[self.length: self.length + len(more_data)] = more_data
        #self._stat[0] += np.sum(more_data, axis=0)
        #self._stat[1] += np.sum(more_data*more_data, axis=0)
        #self._stat[2] += np.sum(more_data[1:]*more_data[:-1], axis=0)
        #if self.length != 0:
        #    self._stat[2] += data[self.length] * more_data[0]
        #self._stat[3] = np.minimum(self._stat[3], np.min(more_data, axis=0))
        #self._stat[4] = np.maximum(self._stat[4], np.max(more_data, axis=0))
        self.length += len(more_data)
        return self

    # appending a single element
    def append(self, elem):
        self += [elem]

    # averaging out over segments
    def reduce_by(self, aver_interval: int):
        """Replace data by its averages over the respective intervals, i.e., array[n] by array[n * size: (n + 1) * size]
        """
        assert self.length % aver_interval == 0, 'the length should be divisible by aver_interval'
        indexes = np.arange(0, self.length, aver_interval)
        self._data = np.add.reduceat(self._data, indexes, axis=0) / aver_interval
        self.length = self.length // aver_interval
        #self_data = self.data()
        #self._stat[0] = np.sum(self_data, axis=0)
        #self._stat[1] = np.sum(self_data*self_data, axis=0)
        #self._stat[2] = np.sum(self_data[1:]*self_data[:-1], axis=0)
        #self._stat[3] = np.min(self_data, axis=0)
        #self._stat[4] = np.max(self_data, axis=0)

class AutoRegr:
    def __init__(self, series: Union[TimeSeries, List[TimeSeries]]):
        """Sets self.rho (Valerr), self.mean (Valerr), self.sigma (float)
        """
        series_list = [series] if isinstance(series, TimeSeries) else series
        data_list = [np.copy(s.data) for s in series_list]
        count = len(series_list)
        width = len(series_list[0].data[0])
        length = sum([len(data) for data in data_list])
        assert length > 6
        av = np.sum([np.sum(data, axis=0) for data in data_list], axis=0) / length
        for i in range(count):
            for j in range(width):
                data_list[i][:,j] -= av[j]
        var = np.sum([np.sum(data * data, axis=0) for data in data_list], axis=0) / length
        cov = np.sum([np.sum(data[1:] * data[:-1], axis=0) for data in data_list], axis=0) / (length-count)
        _min = np.min([np.min(data, axis=0) for data in data_list], axis=0)
        _max = np.max([np.max(data, axis=0) for data in data_list], axis=0)
        max_dev = [max(- _min[i], _max[i]) for i in range(width)]

        rho_err = 1 / np.sqrt(length)
        rho = cov / var; rho[rho<0] = rho_err/3
        sigma = np.sqrt(var - cov * cov / var)
        drop = np.log(-sigma * count / (1-rho) / max_dev / 2 * length**(-3/2) / np.log(rho)) / np.log(rho) # optimal number of points to drop in the beginning
        drop = int(np.ceil(max(drop)))
        while length - drop * count <= 6:
            drop -= 1


        # now repeat again without the leading data
        data_list = [np.copy(s.data[drop:]) for s in series_list]        
        # self.data_list = data_list
        length -= drop * count
        av = np.sum([np.sum(data, axis=0) for data in data_list], axis=0) / length
        for i in range(count):
            for j in range(width):
                data_list[i][:,j] -= av[j]
        var = np.sum([np.sum(data * data, axis=0) for data in data_list], axis=0) / length
        cov = np.sum([np.sum(data[1:] * data[:-1], axis=0) for data in data_list], axis=0) / (length-count)

        self.rho_val = cov / var; self.rho_val[self.rho_val<0] = 0        
        self.sigma = np.sqrt(var - cov * cov / var)
        self.mean_err =  np.sqrt(var * (var + cov) / ((length-6) * (var-cov))) + max_dev * self.rho_val ** drop
        self.mean_val = av
        self.rho_err = np.array([1 / np.sqrt(length) for i in range(width)])

    def __repr__(self):
        return f'<AutoRegr with rho = {self.rho_val} \u00b1 {self.rho_err}, mean = {self.mean_val} \u00b1 {self.mean_err}>'
