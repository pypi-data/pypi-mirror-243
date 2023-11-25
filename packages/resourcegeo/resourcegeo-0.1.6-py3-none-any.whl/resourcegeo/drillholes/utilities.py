'Statistics calculation'

__author__ = 'Harold Velasquez'
__date__ = '2023-07'

import numpy as np

def weighted_avg(values, weights):
    m = np.average(values, weights=weights)
    return m

def weighted_std(values, weights):
    m = weighted_avg(values, weights)
    variance = np.average((values-m)**2, weights=weights)
    return np.sqrt(variance)