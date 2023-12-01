"""Defines basic classes
"""

import numpy as np, random, pathlib, string

temp_dir = pathlib.Path.home() / '.atomica' / 'tmp'
temp_dir.mkdir(exist_ok = True)

class Valerr:
    """Class defining a scalar value with its uncertainty
    """

    def __init__(self, val, err):
        self.val = val
        self.err = err

    def __itruediv__(self, denominator:float):
        self.val /= denominator
        self.err /= denominator
        return self

    def __truediv__(self, denominator:float):
        return Valerr(self.val / denominator, self.err / denominator)

    def __eq__(self, other):
        return (self.val == other.val) and (self.err == other.err)

    def __hash__(self):
      return hash((self.val, self.err))

    def __str__(self):
        digits = int(np.ceil(-np.log10(self.err)+0.3))
        return f'{{:.{digits}f}} ± {{:.{digits}f}}'.format(self.val, self.err)

    def __repr__(self):
        return f'Valerr(val = {self.val}, err = {self.err})'

def temp_file_path(suffix = '') -> pathlib.Path:
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=25))    
    return temp_dir / (random_str + suffix)
