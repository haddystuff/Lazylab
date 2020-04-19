"""Base TinyCore manageconfig class"""
from abc import ABC
import telnetlib
from lazylab.base.base_manage_config import BaseManageConfig
from abc import ABC
import logging


logger = logging.getLogger(__name__)

class TinyCoreManageConfig(BaseManageConfig, ABC):
    """
    This is base TinyCore linux manageconfig class, you have to inherit from it when
    writing new os manage_config class.
    """
    def configure_vm(self):
        print('not added yet')
        pass
    
    def get_vm_config(self):
        print('not added yet')
        pass
