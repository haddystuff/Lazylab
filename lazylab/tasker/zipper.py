"""Zipper module"""
from lazylab.constants import DEVICE_DESCRIPTION_MAIN_STR, LAB_CONFIG_PATH, CONFIG_FILE_NAME
from lazylab.tasker.exceptions import *
from zipfile import ZipFile
import yaml
import logging


logger = logging.getLogger(__name__)

def unzip_lab(lab_name):
    """
    This function finds lab archive and uzip it
    to then returns:
    conf_yaml - config yaml string
    vm_configs - dict with all avalible device configs
    """
    
    # Getting lab file name
    config_archive_name = f'{lab_name}.lazy'
        
    # Getting config_archive_location - lab file location
    config_archive_location = LAB_CONFIG_PATH + config_archive_name
    
    # Creating vm_configs dict
    vm_configs = {}
    
    # Opening config file in zip archive and getting
    # conf_yaml and vm_configs
    try:
        
        with ZipFile(config_archive_location, 'r') as lazy_archive:
            
            zip_files_namelist = lazy_archive.namelist()
            
            # Iterating through all files in archive 
            # and writing its content to vm_configs dictionary
            for zip_file_name in zip_files_namelist:
                vm_configs[zip_file_name] = lazy_archive.read(zip_file_name).decode('utf-8')
            
            # Trying to get config file
            try:
                conf_yaml = vm_configs.get(CONFIG_FILE_NAME)
             
            # If there is no lab configuration file in archive
            # we stop with error
            except KeyError as err:
                logger.warning(f'{err}')
                exit(1)
                                  
    except FileNotFoundError as err:
        logger.info(f'{config_archive_location} not found, trying to download from server')
        raise NoLabArchive(f'Cant find {config_archive_location} archive')

    return conf_yaml, vm_configs;
    
def create_zip_from_string(archive_path, filename, string):
    """This function write new file from string to zip archive."""
    
    config_archive = ZipFile(archive_path, mode="a")
    config_archive.writestr(filename, string)
    config_archive.close() 
    
    return 0
    
def zip_to_archive(conf_dict, vm_configs, lab_archive_path):
    
    with ZipFile(lab_archive_path, 'w') as lazy_archive:
        conf_yaml = yaml.dump(conf_dict)
        lazy_archive.writestr(CONFIG_FILE_NAME, conf_yaml)
        for vm_name, vm_config in vm_configs.items():
            device_config_filename = f'{vm_name}.conf'
            lazy_archive.writestr(device_config_filename, vm_config)
                                    
    return 0

