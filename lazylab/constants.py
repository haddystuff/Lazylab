import os

WAITING_TIMER = 2000
PATH_TO_MODULE = os.path.dirname(os.path.abspath(__file__))
VOLUME_CONFIG_JINJA_TEMPLATE = PATH_TO_MODULE + "/xml_configs/" + "volume_config_jinja_template.xml"
NET_CONFIG_JINJA_TEMPLATE = PATH_TO_MODULE + "/xml_configs/" + 'net_config_jinja_template.xml'
TEMPLATE_VOLUME_POOL_NAME = 'lazylab'
TEMPLATE_VOLUME_POOL_DIRECTORY = PATH_TO_MODULE + '/images/'
MANAGMENT_NET_NAME = 'default'
REMOTE_IMAGE_STORAGE_DIRECTORY_NAME = '/lazylab/images'
REMOTE_LABS_STORAGE_DIRECTORY_NAME = '/lazylab/labs'
LAB_CONFIG_PATH = f'{PATH_TO_MODULE}/labs/'
