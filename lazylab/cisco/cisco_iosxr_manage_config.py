"""Base Cisco IOSXR manageconfig class"""
from lazylab.cisco.cisco_manage_config import CiscoManageConfig
from abc import ABC


class CiscoIOSXRManageConfig(CiscoManageConfig, ABC):
    """
    This is base Cisco IOSXR manageconfig class, you have to inherit from it when writing new specific os version manage_config class.
    """
    
    
    pass
