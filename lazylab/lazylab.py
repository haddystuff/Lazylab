#!/usr/bin/env python3
import sys
from tasker import deploy_lab
from tasker import delete_lab

"""
This is pretty simple UI
Its calling tasker functions
"""

if __name__ == "__main__":
    
    # Checking if argument is define and saving name of zip archive from one of arguments
    if len(sys.argv) == 1:
        print('No argument :(\nPlease use one of this:\n  1.deploy\n  2.delete\n 3.save')
        sys.exit(1)
    elif len(sys.argv) == 2:
        config_archive_location = sys.path[0] + '/labs/' + 'default' + '.lazy'
    elif len(sys.argv) == 3:
        config_archive_location = sys.path[0] + '/labs/' + sys.argv[2] + '.lazy'
    else:
        print('Too many arguments, please use:\n  1.deploy\n  2.delete\n as first argument and directory of configs as second')
        exit(1)
       
    #Parsing arguments and working with manage objects
    if sys.argv[1] == 'deploy':
        deploy_lab(config_archive_location)
            
    elif sys.argv[1] == 'delete':
        delete_lab(config_archive_location)
    #Working on this
    #    elif sys.argv[1] == 'save':
    #        # Save configs
    #        print('savings lab')
    #        for device in devices:
    #            devices[device].save_config_vm()
    else:
        print('Bad argument :(\nPlease use one of this:\n  1.deploy\n  2.delete')
        exit(1)
exit(0)
