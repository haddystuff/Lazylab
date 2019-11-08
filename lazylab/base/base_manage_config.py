import time
from abc import ABC
import sys
from lazylab.config_parser import *

class BaseManageConfig(ABC):
    """
    This is one of base classes you have to inherit from when writing new vendor manage_config class.
    """
    

    def waiting(self):
        #Just waiting method. Its showing animation and sleep as long as needed.
        #Soon we will change it to something more intellectual
        wait_miliseconds = WAITING_TIMERS_COMPARE_TO_CLASS[type(self).__name__]
        animation = "|/-\\"
        for i in range(wait_miliseconds):
            time.sleep(0.1)
            sys.stdout.write("\r" + animation[i % len(animation)])
            sys.stdout.flush()
        return(0)
