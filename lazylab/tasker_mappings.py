from lazylab.cisco.cisco_iosxr_manage_config import CiscoIOSXRManageConfig
from lazylab.juniper.juniper_vmxvcp_manage_config import JuniperVMXVCPManageConfig
from lazylab.juniper.juniper_vmx_manage_config import JuniperVMXManageConfig
from lazylab.base.base_manage_vm import BaseManageVM

OS_TO_CLASS_NAME = {'cisco_iosxr': 'CiscoIOSXR', 
               'juniper_vmx': 'JuniperVMX',
               'juniper_vmxvcp': 'JuniperVMXVCP'}

LAB_ATTRIBUTE_TO_CLASS = {'directory_pool': BaseManageVM}

OS_TO_CLASS = {'cisco_iosxr': CiscoIOSXRManageConfig, 
               'juniper_vmx': JuniperVMXManageConfig,
               'juniper_vmxvcp': JuniperVMXVCPManageConfig}
