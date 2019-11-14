import configparser
import sys
import os
"""
This is config parser. It parses lazylab.conf file also sets static valiables.
"""

#None config constants
PATH_TO_MODULE = os.path.dirname(os.path.abspath(__file__))
POSSIBLE_OS_LIST = ('juniper_vmx_14', 'cisco_iosxr_15')
WAITING_TIMERS_COMPARE_TO_CLASS = {'CiscoIOSXR15ManageAll': 2000, 'JuniperVMX14ManageAll': 1000}
INTERFACE_OFFSET_COMPARE_TO_CLASS = {'CiscoIOSXR15ManageAll': 1, 'JuniperVMX14ManageAll': 2}
INTERFACE_PREFIX_COMPARE_TO_CLASS = {'CiscoIOSXR15ManageAll': 'ge', 'JuniperVMX14ManageAll': 'em'}
DEFAULT_VM_VARIABLE_VALUE = {'name': 'Unknown_VM', 'os': 'Unknown_OS', 'version': 0, 'interfaces': {'ge-0/0/0': 'Unknown_net'}}
VOLUME_CONFIG_JINJA_TEMPLATE = PATH_TO_MODULE + "/xml_configs/" + "volume_config_jinja_template.xml"
NET_CONFIG_JINJA_TEMPLATE = PATH_TO_MODULE + "/xml_configs/" + 'net_config_jinja_template.xml'
TEMPLATE_VOLUME_POOL_NAME = 'lazylab'
TEMPLATE_VOLUME_POOL_DIRECTORY = PATH_TO_MODULE + '/images/'
MANAGMENT_NET_NAME = 'default'

#config constants
config = configparser.ConfigParser()
config.read(PATH_TO_MODULE + '/lazylab.conf')
TELNET_STARTING_PORT = int(config['system']['telnet_starting_port'])
VOLUME_POOL_NAME = config['system']['volume_pool_name']
CONFIG_FILE_NAME = config['system']['config_file_name']
VOLUME_POOL_DIRECTORY = config['system']['volume_pool_directory']
IMAGES_FTP = config['system']['images_ftp']
DEFAULT_PASSWORD = config['passwords']['default_password']

