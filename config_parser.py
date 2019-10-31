import configparser
import sys
"""
This is just a config parser. It parses lazylab.conf file
"""


config = configparser.ConfigParser()
config.read(sys.path[0] + '/lazylab.conf')
TELNET_STARTING_PORT = int(config['system']['telnet_starting_port'])
VOLUME_POOL_NAME = config['system']['volume_pool_name']
CONFIG_FILE_NAME = config['system']['config_file_name']
VOLUME_POOL_DIRECTORY = config['system']['volume_pool_directory']
IMAGES_FTP = config['system']['images_ftp']
DEFAULT_PASSWORD = config['passwords']['default_password']
#None config constants
POSSIBLE_OS_LIST = ('juniper_vmx_14', 'cisco_iosxr_15')
WAITING_TIMERS_COMPARE_TO_CLASS = {'CiscoIOSXR15ManageAll': 2000, 'JuniperVMX14ManageAll': 1000}
