import ftplib
import libvirt
from jinja2 import Template
from lazylab.config_parser import *

def download_template_image(distribution):
    with libvirt.open('qemu:///system') as virt_conn:
        try:
            # Get volume pool
            volume_pool = virt_conn.storagePoolLookupByName(TEMPLATE_VOLUME_POOL_NAME)
            #if there is no pool, i create it
        except Exception as err:
            print(err)                # i expect this: libvirtError('virStoragePoolLookupByName()failed', conn=self)
            #Open jinja2 template file and render it.
            with open(PATH_TO_MODULE + "/xml_configs/" + 'volume_pool_config' + '_jinja_template.xml') as xml_jinja_template:
                template = Template(xml_jinja_template.read())
            config_string = template.render(pool_name = TEMPLATE_VOLUME_POOL_NAME, volume_pool_path = TEMPLATE_VOLUME_POOL_DIRECTORY, owner_uid = str(os.geteuid()), owner_gid = str(os.getegid()))
            # Creating volume pool and adding Autostart
            volume_pool = virt_conn.storagePoolDefineXML(config_string, 0)
            volume_pool.create()
            volume_pool.setAutostart(1)
        
        #downloading images from ftp
        with ftplib.FTP(IMAGES_FTP, 'anonymous', 'anonymous@domain.com') as ftp:
            ftp.cwd(REMOTE_FTP_IMAGE_STORAGE_DIRECTORY_NAME)
            with open(TEMPLATE_VOLUME_POOL_DIRECTORY + distribution + '_template.qcow2', 'wb') as f:
                ftp.retrbinary('RETR ' + distribution + '_template.qcow2', f.write)
        volume_pool.refresh()
    return 0
