"""Base interface for config managers"""
import time
from abc import ABC
import sys
from lazylab.base.base_constants import WAITING_TIMER
import logging


logger = logging.getLogger('lazylab.base.base_manage_config')

class BaseManageConfig(ABC):
    """
    This is one of base classes you have to inherit from when writing new
    vendor specific manage_config class.
    """
    
    
    def waiting(self):
        """This method showing animation and sleep as long as needed"""
        
        logger.info('starting dump waiting method')
        wait_miliseconds = WAITING_TIMER
        animation = "|/-\\"
        for i in range(wait_miliseconds):
            time.sleep(0.1)
            sys.stdout.write("\r" + animation[i % len(animation)])
            sys.stdout.flush()
        return 0
