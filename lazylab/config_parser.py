"""Config parser"""
import configparser
import logging
from lazylab.constants import *


logger = logging.getLogger(__name__)

# logging
logger.info('starting parsing')

# parsing
config = configparser.ConfigParser()
config.read(PATH_TO_MODULE + '/lazylab.conf')
TELNET_STARTING_PORT = int(config['system']['telnet_starting_port'])
VOLUME_POOL_NAME = config['system']['volume_pool_name']
CONFIG_FILE_NAME = config['system']['config_file_name']
VOLUME_POOL_DIRECTORY = config['system']['volume_pool_directory']
IMAGES_SERVER = config['system']['images_server']
LABS_SERVER = config['system']['labs_server']
PASSWORD_LIST = config.items( "passwords" )
