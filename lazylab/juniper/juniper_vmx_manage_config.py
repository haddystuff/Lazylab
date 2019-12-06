from lazylab.juniper.juniper_manage_config import JuniperManageConfig
from abc import ABC

class JuniperVMXManageConfig(JuniperManageConfig, ABC):
    """
    This is base juniper VMX manageconfig class, you have to inherit from it when writing new specific os version manage_config class.
    """
    
    pass
