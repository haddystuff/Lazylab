"""Constants file"""
import os

WAITING_TIMER = 2000
PATH_TO_MODULE = os.path.dirname(os.path.abspath(__file__))
VOLUME_CONFIG_TEMPLATE_NAME = "volume_config_jinja_template.xml"
TEMPLATE_DIRECTORY_PATH = PATH_TO_MODULE + "/xml_configs"
NET_CONFIG_TEMPLATE_NAME = 'net_config_jinja_template.xml'
POOL_CONFIG_TEMPLATE_NAME = 'volume_pool_config_jinja_template.xml'
TEMPLATE_VOLUME_POOL_NAME = 'lazylab'
TEMPLATE_VOLUME_POOL_DIRECTORY = PATH_TO_MODULE + '/images/'
MANAGMENT_NET_NAME = 'default'
REMOTE_IMAGE_STORAGE_DIRECTORY_NAME = '/lazylab/images'
REMOTE_LABS_STORAGE_DIRECTORY_NAME = '/lazylab/labs'
LAB_CONFIG_PATH = f'{PATH_TO_MODULE}/labs/'

TEMPLATE_IMAGE_LIST = {'juniper_vmx_14': ['juniper_vmx_14_template.qcow2'],
                       'juniper_vmxvcp_18': ['juniper_vmxvcp_18_A_template.qcow2', 
                                             'juniper_vmxvcp_18_B_template.qcow2', 
                                             'juniper_vmxvcp_18_C_template.qcow2'],
                       'cisco_iosxr_15': ['cisco_iosxr_15_template.qcow2']}
                      
INTERFACE_OFFSET = {'cisco_iosxr_15': 1,
                    'juniper_vmx_14': 2,
                    'juniper_vmxvcp_18': 2}

INTERFACE_PREFIX = {'cisco_iosxr_15': 'ge',
                    'juniper_vmx_14': 'em',
                    'juniper_vmxvcp_18': 'ge'}
                    
POSSIBLE_OS_LIST = ('juniper_vmx_14',
                    'cisco_iosxr_15', 
                    'juniper_vmxvcp_18')
                    
DEVICE_DESRIPTION_MAIN_STR = '#Auto-generated vm with lazylab'
