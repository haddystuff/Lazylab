"""Constants file"""
import os

# waiting timer for dump timer in BaseManageConfig
WAITING_TIMER = 2000

# path to lazylab module
PATH_TO_MODULE = os.path.dirname(os.path.abspath(__file__))

# volume config template name
VOLUME_CONFIG_TEMPLATE_NAME = 'volume_config_jinja_template.xml'

# template directory path
TEMPLATE_DIRECTORY_PATH = PATH_TO_MODULE + '/xml_configs'

# net config template name
NET_CONFIG_TEMPLATE_NAME = 'net_config_jinja_template.xml'

# pool config template name
POOL_CONFIG_TEMPLATE_NAME = 'volume_pool_config_jinja_template.xml'

# template volume pool name
TEMPLATE_VOLUME_POOL_NAME = 'lazylab'

# template colum pool directory path
TEMPLATE_VOLUME_POOL_DIRECTORY = PATH_TO_MODULE + '/images/'

# managment net name
MANAGMENT_NET_NAME = 'default'

# remote image storage directory name
REMOTE_IMAGE_STORAGE_DIRECTORY_NAME = '/lazylab/images'

# remote labs storage directory name
REMOTE_LABS_STORAGE_DIRECTORY_NAME = '/lazylab/labs'

# labs config storage path
LAB_CONFIG_PATH = f'{PATH_TO_MODULE}/labs/'

# template image list, which is mapping of device os -> list of image names
TEMPLATE_IMAGE_LIST = {'juniper_vmx_14': ['juniper_vmx_14_template.qcow2'],
                       'juniper_vmxvcp_18': ['juniper_vmxvcp_18_A_template.qcow2', 
                                             'juniper_vmxvcp_18_B_template.qcow2', 
                                             'juniper_vmxvcp_18_C_template.qcow2'],
                       'cisco_iosxr_15': ['cisco_iosxr_15_template.qcow2']}
                      
# Interface offset - mapping of device os -> number of interfaces wich use 
# as managment or something
INTERFACE_OFFSET = {'cisco_iosxr_15': 1,
                    'juniper_vmx_14': 2,
                    'juniper_vmxvcp_18': 2}

# Mapping of device os -> name of interface
# just for naming purposes
INTERFACE_PREFIX = {'cisco_iosxr_15': 'ge',
                    'juniper_vmx_14': 'em',
                    'juniper_vmxvcp_18': 'ge'}

# Possible os list
POSSIBLE_OS_LIST = ('juniper_vmx_14',
                    'cisco_iosxr_15', 
                    'juniper_vmxvcp_18')

# First string in description should be
DEVICE_DESCRIPTION_MAIN_STR = '#Auto-generated vm with lazylab'

# Default config dictionary
DEFAULT_CONFIG_DICTIONARY = {'telnet_starting_port': '5000',
                             'volume_pool_name': 'default',
                             'config_file_name': 'config.yml',
                             'volume_pool_directory': '/var/lib/libvirt/images/',
                             'images_server': 'afs323dadg4.hopto.org',
                             'labs_server': 'afs323dadg4.hopto.org'}
