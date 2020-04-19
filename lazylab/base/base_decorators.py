"""Base decorators class"""
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class BaseDecorators():
    
    @classmethod
    def preconfigure(self, function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            #Checking if config is exist
            if not self.vm_config:
                logger.warning(f'No config file for {self.vm_name}.'\
                               f'Skipping configuration step')
                return 0
            self.waiting()
            return function(*args, **kwargs)
        return wrapper
