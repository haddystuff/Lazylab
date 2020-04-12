"""Downloader"""
import ftplib
import libvirt
import logging
import os
from jinja2 import Environment, FileSystemLoader
from lazylab.config_parser import *
from lazylab.constants import TEMPLATE_DIRECTORY_PATH, POOL_CONFIG_TEMPLATE_NAME, TEMPLATE_IMAGE_LIST, TEMPLATE_VOLUME_POOL_DIRECTORY

# Create logger
logger = logging.getLogger(__name__)

# Create enviroment for jinja2
env = Environment(loader=FileSystemLoader(TEMPLATE_DIRECTORY_PATH))

def download_template_image(template_volume_name):
    """
    this function downloading templates from ftp server(can change it in 
    config file)
    """
    
    with libvirt.open('qemu:///system') as virt_conn:
       
        try:
            # Get volume pool
            volume_pool = virt_conn.storagePoolLookupByName(TEMPLATE_VOLUME_POOL_NAME)
            
        #if there is no pool, i create it
        except libvirt.libvirtError as err:
            
            # exit if its unexpected error
            if err.get_error_code() != 49: # 49 is error message for "storage pool not found"
                logger.error(f'{err.get_error_message()}')
                exit(1)
            
            # Getting jinja2 template file
            template = env.get_template(POOL_CONFIG_TEMPLATE_NAME)
                
            # Rendering jinja2 template
            config_string = template.render(pool_name = TEMPLATE_VOLUME_POOL_NAME, 
                                            volume_pool_path = TEMPLATE_VOLUME_POOL_DIRECTORY, 
                                            owner_uid = str(os.geteuid()), 
                                            owner_gid = str(os.getegid()))
            
            # Creating volume pool and adding Autostart
            volume_pool = virt_conn.storagePoolDefineXML(config_string, 0)
            volume_pool.create()
            volume_pool.setAutostart(1)
        
        # connecting to ftp server
        with ftplib.FTP(IMAGES_SERVER, 'anonymous', 'anonymous@domain.com') as ftp:
            
            # locating remote dir
            ftp.cwd(REMOTE_IMAGE_STORAGE_DIRECTORY_NAME)
            
            # Creating file in local storage
            with open(TEMPLATE_VOLUME_POOL_DIRECTORY + template_volume_name, 'wb') as f:
                
                # Writing data from ftp to file
                ftp.retrbinary('RETR ' + template_volume_name, f.write)
                
        # Refreshing volume pool
        volume_pool.refresh()
        
    return 0


def download_lab_config_file(lab_name):
    """
    This function downloading lab config file from ftp server(can change it in 
    config file)
    """
    
    config_archive_name = f'{lab_name}.lazy'
    print(f'trying to download {config_archive_name}')
        
    # connecting to ftp server
    with ftplib.FTP(LABS_SERVER, 'anonymous', 'anonymous@domain.com') as ftp:
        
        # locating remote dir
        ftp.cwd(REMOTE_LABS_STORAGE_DIRECTORY_NAME)
        
        # Creating file on local storage
        with open(LAB_CONFIG_PATH + config_archive_name, 'wb') as f:
            
            # Writing data from ftp to file
            ftp.retrbinary('RETR ' + config_archive_name, f.write)
            
    return 0
    
    
def check_images(conf_dict):
    """
    This function check if template images exist, if not it running 
    download_template_image function wich download image.
    """
    
    #Getting vms_parameters_list
    vms_parameters_list = conf_dict.get('vms')
    
    # Check if image of os exist on local disk
    for vm_parameters in vms_parameters_list:
        
        logger.info('checking if {distribution} template image exist')
        
        # Getting distribution
        distribution = vm_parameters.get('os') + '_' + str(vm_parameters.get('version'))
    
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
