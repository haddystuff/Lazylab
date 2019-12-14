"""Base Juniper vmxvcp manageconfig class"""
from lazylab.juniper.juniper_manage_config import JuniperManageConfig
from abc import ABC

class JuniperVMXVCPManageConfig(JuniperManageConfig, ABC):
    """
    This is base juniper VMXVCP manageconfig class, you have to inherit from it
    when writing new specific os version manage_config class.
    """
    
    pass
