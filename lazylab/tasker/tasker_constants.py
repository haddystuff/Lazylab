"""Tasker constants"""
from lazylab.cisco.cisco_iosxr_manage_config import CiscoIOSXRManageConfig
from lazylab.juniper.juniper_vmxvcp_manage_config import JuniperVMXVCPManageConfig
from lazylab.juniper.juniper_vmx_manage_config import JuniperVMXManageConfig
from lazylab.tinycore.tinycore_custom_manage_config import TinyCoreCustomManageConfig
from lazylab.base.base_persistency_support import BasePersistencySupport
from lazylab.base.base_qcow_support import BaseQcowSupport

# OS to class name mapper
OS_TO_CLASS_NAME = {'cisco_iosxr': 'CiscoIOSXR', 
               'juniper_vmx': 'JuniperVMX',
               'tinycore_custom': 'TinyCoreCustom',
               'juniper_vmxvcp': 'JuniperVMXVCP'}

# Lab attribute to class mapper
LAB_ATTRIBUTE_TO_CLASS = {'qcow': BaseQcowSupport,
                          'persistent': BasePersistencySupport}

# os to class mapper
OS_TO_CLASS = {'cisco_iosxr': CiscoIOSXRManageConfig, 
               'juniper_vmx': JuniperVMXManageConfig,
               'tinycore_custom': TinyCoreCustomManageConfig,
               'juniper_vmxvcp': JuniperVMXVCPManageConfig}
