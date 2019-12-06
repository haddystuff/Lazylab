import time
from abc import ABC
import sys
from lazylab.constants import WAITING_TIMER
import logging


logger = logging.getLogger('lazylab.base.base_manage_config')

class BaseManageConfig(ABC):
    """
    This is one of base classes you have to inherit from when writing new
    vendor manage_config class.
    """
    

    def waiting(self):
        #Just waiting method. Its showing animation and sleep as long as needed
        #Soon we will change it to something more intellectual
        wait_miliseconds = WAITING_TIMER
        animation = "|/-\\"
        for i in range(wait_miliseconds):
            time.sleep(0.1)
            sys.stdout.write("\r" + animation[i % len(animation)])
            sys.stdout.flush()
        return 0
