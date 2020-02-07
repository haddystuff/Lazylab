"""Config parser"""
import configparser
import logging
from lazylab.constants import DEFAULT_CONFIG_DICTIONARY, PATH_TO_MODULE

# logging
logger = logging.getLogger(__name__)
logger.info('starting parsing config')

# create parser and read file
config = configparser.ConfigParser()
config.read(PATH_TO_MODULE + '/lazylab.conf')

# Getting 'system' section from config file as dict
try:
    system_config = config['system']
    
except KeyError:
    logger.warning('No \'system\' section in config file, using default dict')
    system_config = DEFAULT_CONFIG_DICTIONARY

# Telnet port to start from
TELNET_STARTING_PORT = int(system_config.get('telnet_starting_port', '5000'))

# Volume pool name
VOLUME_POOL_NAME = system_config.get('volume_pool_name', 'default')

# Volume pool dir
VOLUME_POOL_DIRECTORY = system_config.get('volume_pool_directory', '/var/lib/libvirt/images/')

# image server
IMAGES_SERVER = system_config.get('images_server', 'afs323dadg4.hopto.org')

# Server with lab config gile to download
LABS_SERVER = system_config.get('labs_server', 'afs323dadg4.hopto.org')

# list of passwords
PASSWORD_LIST = config.items('passwords', ['Lazylab1'])
