import configparser
import sys
import os
"""
This is config parser. It parses lazylab.conf file also sets static valiables.
"""

#None config constants
PATH_TO_MODULE = os.path.dirname(os.path.abspath(__file__))
POSSIBLE_OS_LIST = ('juniper_vmx_14', 'cisco_iosxr_15', 'juniper_vmxvcp_18')
WAITING_TIMERS_COMPARE_TO_CLASS = {'CiscoIOSXR15ManageAll': 2000, 
                                   'JuniperVMX14ManageAll': 1000,
                                   'JuniperVMXVCP18ManageAll': 1500}
INTERFACE_OFFSET_COMPARE_TO_CLASS = {'CiscoIOSXR15ManageAll': 1,
                                     'JuniperVMX14ManageAll': 2,
                                     'JuniperVMXVCP18ManageAll': 2}
INTERFACE_PREFIX_COMPARE_TO_CLASS = {'CiscoIOSXR15ManageAll': 'ge',
                                     'JuniperVMX14ManageAll': 'em',
                                     'JuniperVMXVCP18ManageAll': 'ge'}
DISTRIBUTION_COMPARE_TO_IMAGE = {'juniper_vmx_14': ['juniper_vmx_14_template.qcow2'],
                                 'juniper_vmxvcp_18': ['juniper_vmxvcp_18_A_template.qcow2', 'juniper_vmxvcp_18_B_template.qcow2', 'juniper_vmxvcp_18_C_template.qcow2'],
                                 'cisco_iosxr_15': ['cisco_iosxr_15_template.qcow2']}
DEFAULT_VM_VARIABLE_VALUE = {'name': 'Unknown_VM', 'os': 'Unknown_OS', 'version': 0, 'interfaces': {'ge-0/0/0': 'Unknown_net'}}
VOLUME_CONFIG_JINJA_TEMPLATE = PATH_TO_MODULE + "/xml_configs/" + "volume_config_jinja_template.xml"
NET_CONFIG_JINJA_TEMPLATE = PATH_TO_MODULE + "/xml_configs/" + 'net_config_jinja_template.xml'
TEMPLATE_VOLUME_POOL_NAME = 'lazylab'
TEMPLATE_VOLUME_POOL_DIRECTORY = PATH_TO_MODULE + '/images/'
MANAGMENT_NET_NAME = 'default'
REMOTE_FTP_IMAGE_STORAGE_DIRECTORY_NAME = '/lazylab'

#config constants
config = configparser.ConfigParser()
config.read(PATH_TO_MODULE + '/lazylab.conf')
TELNET_STARTING_PORT = int(config['system']['telnet_starting_port'])
VOLUME_POOL_NAME = config['system']['volume_pool_name']
CONFIG_FILE_NAME = config['system']['config_file_name']
VOLUME_POOL_DIRECTORY = config['system']['volume_pool_directory']
IMAGES_FTP = config['system']['images_ftp']
PASSWORD_LIST = config.items( "passwords" )
