#!/usr/bin/env python3
import lazylab
import sys
from lazylab.tasker import deploy_lab
from lazylab.tasker import delete_lab
from lazylab.tasker import save_lab
from lazylab.config_parser import *
import logging


"""
This is pretty simple UI. We need to complitely rewrite it
Its calling tasker functions
"""


# Create a custom logger
logger = logging.getLogger('lazylab')
# Create logger handler
logger_handler = logging.StreamHandler()
# set logging level
logger_handler.setLevel(logging.WARNING)
# set format
output_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
logger_handler.setFormatter(output_format)
# set logger handler
logger.addHandler(logger_handler)

def main():
    
    # We need to completely rewrite this UI
    # Checking if argument is define and saving name of zip archive from one of arguments
    if len(sys.argv) == 1:
        print('No argument :(\nPlease use one of this:\n  1.deploy\n  2.delete\n 3.save')
        sys.exit(1)
    elif len(sys.argv) == 2:
        config_archive_location = PATH_TO_MODULE + '/labs/' + 'default' + '.lazy'
    elif len(sys.argv) == 3:
        config_archive_location = PATH_TO_MODULE + '/labs/' + sys.argv[2] + '.lazy'
    # else:
        # print('Too many arguments, please use:\n  1.deploy\n  2.delete\n as first argument and directory of configs as second')
        # exit(1)
       
    #Parsing arguments and working with manage objects
    if sys.argv[1] == 'deploy':
        logger.debug('Deploying lab')
        deploy_lab(config_archive_location)
            
    elif sys.argv[1] == 'delete':
        logger.debug('Deleting lab')
        lab_name = sys.argv[2]
        delete_lab(lab_name)
    
    elif (sys.argv[1] == 'save') and (sys.argv[3] == 'as'):
        # Save configs
        logger.debug('saving lab')
        old_lab_name = sys.argv[2]
        new_lab_name = sys.argv[4]
        save_lab(old_lab_name, new_lab_name)
    else:
        print('Bad argument :(\nPlease use one of this:\n  1.deploy\n  2.delete')
        exit(1)
    exit(0)

if __name__ == "__main__":
    main()
