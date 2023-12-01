__version__ = "0.3"
__author__ = "Thomas Baldauf"
__email__ = "thomas.baldauf@dlr.de"
__license__ = "MIT"
__birthdate__ = '15.11.2021'
__status__ = 'prod' # options are: dev, test, prod

import warnings

class Singleton(object):
    """
    Plain vanilla singleton class
    """
    _instance = None
    __initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls) #  , *args, **kwargs)

            for k,v in kwargs.items():
                # print("setattr", k, v)
                if not hasattr(cls._instance,k):
                    cls._instance.__dict__[k] = v  # (k,v)
                else:
                    warnings.warn("Cannot re-set singleton attribute %s. Skipping..." % str(k))
                    # NOTE this should actually not be reached 

        return cls._instance
    
    def __init__(self, *args, **kwargs):
        pass

    @property
    def do_init(self):
        return not self.__initialized

    def set_initialized(self):
        self.__initialized = True

    def let_die(self):
        self.__initialized = False 
        self._instance = None 