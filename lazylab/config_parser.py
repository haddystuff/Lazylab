import configparser
import sys
import os
"""
This is just a config parser. It parses lazylab.conf file
"""

PATH_TO_MODULE = os.path.dirname(os.path.abspath(__file__))

config = configparser.ConfigParser()
config.read(PATH_TO_MODULE + '/lazylab.conf')
TELNET_STARTING_PORT = int(config['system']['telnet_starting_port'])
VOLUME_POOL_NAME = config['system']['volume_pool_name']
CONFIG_FILE_NAME = config['system']['config_file_name']
VOLUME_POOL_DIRECTORY = config['system']['volume_pool_directory']
IMAGES_FTP = config['system']['images_ftp']
DEFAULT_PASSWORD = config['passwords']['default_password']
#None config constants
POSSIBLE_OS_LIST = ('juniper_vmx_14', 'cisco_iosxr_15')
WAITING_TIMERS_COMPARE_TO_CLASS = {'CiscoIOSXR15ManageAll': 2000, 'JuniperVMX14ManageAll': 1000}
DEFAULT_VM_VARIABLE_VALUE = {'name': 'Unknown_VM', 'os': 'Unknown_OS', 'version': 0, 'interfaces': {'ge-0/0/0': 'Unknown_net'}}
VOLUME_CONFIG_JINJA_TEMPLATE = PATH_TO_MODULE + "/xml_configs/" + "volume_config_jinja_template.xml"
NET_CONFIG_JINJA_TEMPLATE = PATH_TO_MODULE + "/xml_configs/" + 'net_config_jinja_template.xml'
