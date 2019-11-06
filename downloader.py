import ftplib
from config_parser import *

def download_template_image(distribution):
    with ftplib.FTP(IMAGES_FTP, 'anonymous', 'anonymous@domain.com') as ftp:
        ftp.cwd('/pub')
        with open(VOLUME_POOL_DIRECTORY + distribution + '_template.qcow2', 'wb') as f:
            ftp.retrbinary('RETR ' + distribution + '_template.qcow2', f.write)
    return(0)
