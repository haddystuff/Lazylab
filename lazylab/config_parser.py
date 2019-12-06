import configparser
import sys
import os
"""
This is config parser. It parses lazylab.conf file also sets static valiables.
"""

#None config constants
PATH_TO_MODULE = os.path.dirname(os.path.abspath(__file__))

POSSIBLE_OS_LIST = ('juniper_vmx_14',
                    'cisco_iosxr_15', 
                    'juniper_vmxvcp_18')

WAITING_TIMER = 2000
                

INTERFACE_OFFSET = {'cisco_iosxr_15': 1,
                    'juniper_vmx_14': 2,
                    'juniper_vmxvcp_18': 2}

INTERFACE_PREFIX = {'cisco_iosxr_15': 'ge',
                    'juniper_vmx_14': 'em',
                    'juniper_vmxvcp_18': 'ge'}

DISTRIBUTION_IMAGE = {'juniper_vmx_14': ['juniper_vmx_14_template.qcow2'],
                      'juniper_vmxvcp_18': ['juniper_vmxvcp_18_A_template.qcow2', 
                                            'juniper_vmxvcp_18_B_template.qcow2', 
                                            'juniper_vmxvcp_18_C_template.qcow2'],
                      'cisco_iosxr_15': ['cisco_iosxr_15_template.qcow2']}

DEFAULT_VM_PARAMETERS = {'name': 'Unknown_VM', 
                         'os': 'Unknown_OS',
                         'version': 0, 
                         'interfaces': {'ge-0/0/0': 'Unknown_net'}}

VOLUME_CONFIG_JINJA_TEMPLATE = PATH_TO_MODULE + "/xml_configs/" + "volume_config_jinja_template.xml"
NET_CONFIG_JINJA_TEMPLATE = PATH_TO_MODULE + "/xml_configs/" + 'net_config_jinja_template.xml'
TEMPLATE_VOLUME_POOL_NAME = 'lazylab'
TEMPLATE_VOLUME_POOL_DIRECTORY = PATH_TO_MODULE + '/images/'
MANAGMENT_NET_NAME = 'default'
REMOTE_IMAGE_STORAGE_DIRECTORY_NAME = '/lazylab/images'
REMOTE_LABS_STORAGE_DIRECTORY_NAME = '/lazylab/labs'

#config constants
config = configparser.ConfigParser()
config.read(PATH_TO_MODULE + '/lazylab.conf')
TELNET_STARTING_PORT = int(config['system']['telnet_starting_port'])
VOLUME_POOL_NAME = config['system']['volume_pool_name']
CONFIG_FILE_NAME = config['system']['config_file_name']
VOLUME_POOL_DIRECTORY = config['system']['volume_pool_directory']
IMAGES_SERVER = config['system']['images_server']
LABS_SERVER = config['system']['labs_server']
PASSWORD_LIST = config.items( "passwords" )
LAB_CONFIG_PATH = f'{PATH_TO_MODULE}/labs/'
