# Mapping object for holding upper and lower error bars
#
# Author: Zach Sailer
#
# ----------------------------------------------------------
# Local imports
# ----------------------------------------------------------

import numpy as np

from seqspace.base import BaseMap


class BaseErrorMap(BaseMap):
    
    def __init__(self, phenotypes, stdeviations, log_transform=False, lower=None):
        """ If a lower bound is given, use it instead of -variances. """
        
        self.phenotypes = phenotypes
        self.stdeviations = stdeviations
        self.log_transform = log_transform
    
        # Set a lower bound -- if None, just use upper bound.
        self.stdeviations_ = lower
        if lower == None:
            self.steviations_ = self.stdeviations   
        
    
    @staticmethod
    def transform(bounds, phenotypes):
        """ Log transformation scaling. 
        
            Untransformed data looks as so:
                
                Yupper = Ymean + bound
                Ylower = Ymean - bound
                
            We want log(bounds)
                ie.
                    log(Yupper) - log(Ymean)
                    log(Ylower) + log(Ymean)
                
            so log(bound) = log(1 + bound/Ymean)
               log(bound) = log(1 - bound/Ymean)
        """
        return abs(np.log10(1 + bounds/phenotypes))
        
    @staticmethod
    def wrapper(bound, **kwargs):
        """ Wrapper function that changes variances to whatever bound desired. """
        raise Exception(""" Must be implemented in a subclass """)
    
    @property
    def upper(self):
        """"""
        if self.log_transform:
            return self.transform(self.wrapper(self.stdeviations), self.phenotypes)
        else:
            return self.wrapper(self.stdeviations)
        
    @property
    def lower(self):
        """"""
        if self.log_transform:
            return self.transform(-self.wrapper(self.stdeviations), self.phenotypes)
        else:
            return self.wrapper(self.stdeviations_) 
            

class StandardDeviationMap(BaseErrorMap):
    
    def __init__(self, phenotypes, stdeviations, log_transform=False, lower=None):
        """ Initialize a standard deviations map. """
        super(StandardDeviationMap, self).__init__(phenotypes, stdeviations, log_transform=log_transform, lower=lower)

    @staticmethod
    def wrapper(bounds, **kwargs):
        """ Wrapper function to convert Variances if necessary"""
        return bounds

class StandardErrorMap(BaseErrorMap):
    
    def __init__(self, phenotypes, variances, log_transform=False, n_replicates=2, lower=None):
        """ Initialize a standard error map object """
        super(StandardErrorMap, self).__init__(phenotypes, variances, log_transform=log_transform, lower=lower)
        self.n_replicates = n_replicates
        
    @staticmethod
    def wrapper(bounds, n_replicates=2):
        """ Wrapper function to convert Variances if necessary"""
        return bounds/np.sqrt(n_replicates)