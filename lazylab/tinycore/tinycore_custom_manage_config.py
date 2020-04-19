"""Base Tiny Core Linux manageconfig class"""
from lazylab.tinycore.tinycore_manage_config import TinyCoreManageConfig
from abc import ABC


class TinyCoreCustomManageConfig(TinyCoreManageConfig, ABC):
    """
    This is base Tiny Core custom image manageconfig class, you have to inherit from it 
    when writing new specific os version manage_config class.
    """
    
    
    pass
