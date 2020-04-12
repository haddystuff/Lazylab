#!/usr/bin/env python3
import lazylab
import sys
from lazylab.tasker.tasker import Tasker
import logging


"""
This is pretty gabage UI. We need to complitely rewrite it from scratch.
Its calling tasker functions
"""

# Create a custom logger
logger = logging.getLogger("lazylab")
#Set level
logger.setLevel(logging.INFO)
# Create logger handler
logger_handler = logging.StreamHandler()
# set format
output_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
logger_handler.setFormatter(output_format)
# set logger handler
logger.addHandler(logger_handler)

def main():
    """ We need to completely rewrite this UI"""
    
    logger.info('starting main function')
    
    # Checking if argument is define and saving name of zip archive from one of arguments
        
    if len(sys.argv) == 1:
        print('No argument :(\nPlease use one of this:\n  1.deploy\n  2.delete\n 3.save')
        sys.exit(1)
    elif len(sys.argv) == 2:
        lab_name = 'default'
    elif len(sys.argv) == 3:
        lab_name = sys.argv[2]
    # else:
        # print('Too many arguments, please use:\n  1.deploy\n  2.delete\n as first argument and directory of configs as second')
        # exit(1)
       
    #Parsing arguments and working with manage objects
    task = Tasker()
    if sys.argv[1] == 'deploy':
        logger.debug('Deploying lab')
        task.deploy_lab(lab_name)
            
    elif sys.argv[1] == 'delete':
        logger.debug('Deleting lab')
        task.delete_lab(lab_name)
    
    elif (sys.argv[1] == 'save') and (sys.argv[3] == 'as'):
        # Save configs
        logger.debug('saving lab')
        old_lab_name = sys.argv[2]
        new_lab_name = sys.argv[4]
        task.save_lab(old_lab_name, new_lab_name)
    else:
        print('Bad argument :(\nPlease use one of this:\n  1.deploy\n  2.delete')
        exit(1)
    exit(0)

if __name__ == "__main__":
    main()
