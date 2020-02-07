"""Tasker helpers functions"""
import socket
import logging
import os
from lazylab.downloader import download_template_image
from lazylab.constants import TEMPLATE_IMAGE_LIST, TEMPLATE_VOLUME_POOL_DIRECTORY, POSSIBLE_OS_LIST
from zipfile import ZipFile


logger = logging.getLogger(__name__)

def is_port_in_use(port):
    """This function returns True if socket in use and false if not"""
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        return s.connect_ex(('localhost', port)) == 0
        
        
def create_zip_from_string(archive_path, filename, string):
    """This function write new file from string to zip archive."""
    
    config_archive = ZipFile(archive_path, mode="a")
    config_archive.writestr(filename, string)
    config_archive.close() 
    
    return 0
    

def check_if_template_images_exist(distribution):
    """
    This function check if template images exist, if not it running 
    download_template_image function wich download image.
    """
    
    logger.info('checking if {distribution} template image exist')
    
    # Getting volume base on distribution
    volume_list = TEMPLATE_IMAGE_LIST.get(distribution)
    
    logger.info('we need this images: {volume_list}')
    
    # Iterating through volume list
    for template_volume_name in volume_list:
        
        # Checking file existence
        if os.path.isfile(TEMPLATE_VOLUME_POOL_DIRECTORY + template_volume_name):
            
            logger.info('{template_volume_name} image exist')
            
        else:
            
            logger.info('{template_volume_name} image dont exist')
            print('No ' + distribution + ' image\nDownloading...')
            
            # Downloading image
            download_template_image(template_volume_name)
            
    return 0


def yaml_validate(conf_yaml):
    """
    This function check if yaml file has right structure and syntax.
    We need to modify this code so we can check all syntax in yaml file.
    """
    
    # Getting list of vms.
    vms_parameters_list = conf_yaml.get('vms')
    
    # Check if vms is actualy existing
    if vms_parameters_list is None:
        print('No \"vms\" block in config file')
        exit(1)
    
    # Check if lab name existing
    if conf_yaml.get('lab_name') is None:
        print('No \"lab_name\" block in config file')
        exit(1)
    
    # Check vm one by one.
    for vm_parameters in vms_parameters_list:
        
        # Check if name of vm is actially exist
        if vm_parameters.get('name') is None:
            print('No \"VM Name\" block in config file')
            exit(1)
        
        # Check if vm has right os and version(distibution in this context)
        distribution = vm_parameters.get('os') + '_' + str(vm_parameters.get('version'))
        
        if not(distribution in POSSIBLE_OS_LIST):
            print('Yaml file has bad syntax: wrong os name')
            exit(1)
        
        # Check if image of os exist on local disk
        check_if_template_images_exist(distribution)
        
    return 0
