"""Downloader"""
import ftplib
import libvirt
import logging
from jinja2 import Environment, FileSystemLoader
from lazylab.config_parser import *
from lazylab.constants import TEMPLATE_DIRECTORY_PATH, POOL_CONFIG_TEMPLATE_NAME


logger = logging.getLogger(__name__)

# Create enviroment for jinja2
env = Environment(loader=FileSystemLoader(TEMPLATE_DIRECTORY_PATH))

def download_template_image(template_volume_name):
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
        
        # downloading images from ftp
        with ftplib.FTP(IMAGES_SERVER, 'anonymous', 'anonymous@domain.com') as ftp:
            ftp.cwd(REMOTE_IMAGE_STORAGE_DIRECTORY_NAME)
            with open(TEMPLATE_VOLUME_POOL_DIRECTORY + template_volume_name, 'wb') as f:
                ftp.retrbinary('RETR ' + template_volume_name, f.write)
        volume_pool.refresh()
    return 0

def download_lab_config_file(config_archive_name):
    print(f'trying to download {config_archive_name}')
    with ftplib.FTP(LABS_SERVER, 'anonymous', 'anonymous@domain.com') as ftp:
        ftp.cwd(REMOTE_LABS_STORAGE_DIRECTORY_NAME)
        with open(LAB_CONFIG_PATH + config_archive_name, 'wb') as f:
            ftp.retrbinary('RETR ' + config_archive_name, f.write)
    return 0
