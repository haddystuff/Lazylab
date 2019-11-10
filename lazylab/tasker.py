import yaml
from lazylab.juniper.juniper_vmx_14_manage_all import JuniperVMX14ManageAll
from lazylab.cisco.cisco_iosxr_15_manage_all import CiscoIOSXR15ManageAll
from lazylab.config_parser import *
from zipfile import ZipFile
import os
from lazylab.downloader import download_template_image

"""
This file contain business logic functions that called from UI 
"""


def check_if_template_image_exist(distribution):
    if os.path.isfile(TEMPLATE_VOLUME_POOL_DIRECTORY + distribution + '_template.qcow2'):
        return(0)
    else:
        print('No' + distribution + 'image\nDownloading...')
        download_template_image(distribution)


def yaml_validate(conf_yaml):
    """
    This function check if yaml file has right structure
    """
    #Getting list of vms
    list_of_vms = conf_yaml["vms"]
    
    #Check if vms is actualy existing
    if list_of_vms == None:
        print("No \"vms\" block in config file")
        exit(1)
    #Check if lab name existing
    if conf_yaml["lab_name"] == None:
        print("No \"lab_name\" block in config file")
        exit(1)
    
    #Check vm one by one.
    for vm in list_of_vms:
        #Check if name of vm is actially exist
        if vm['name'] == None:
            print("No \"VM Name\" block in config file")
            exit(1)
        
        #Check if vm has right os and version(distibution in this context)
        distribution = vm['os'] + '_' + str(vm['version'])
        
        if not(distribution in POSSIBLE_OS_LIST):
            print('Yaml file has bad syntax: wrong os name')
            exit(1)
        
        #Check if image of os exist on local disk
        check_if_template_image_exist(distribution)
    return(0)


def create_device_dict_with_archive(config_archive_location):
    """
    This function creating dict of manage objects from zip archive. It actially looks like this:
    { Testlab_router1: CiscoIOSXR15ManageAll_object
      Testlab_router2: JuniperVMX14ManageAll_object
    }
    """
    #Opening config file in zip archive, parsing with yaml and sending to conf_yaml valiable
    with ZipFile(config_archive_location, 'r') as lazy_archive:
        conf_yaml = yaml.load(lazy_archive.read(CONFIG_FILE_NAME), Loader=yaml.FullLoader)
    
    #Validating syntax and more of conf_yaml
    yaml_validate(conf_yaml)
    
    #Setting some valiables
    lab_name = conf_yaml["lab_name"]
    cur_port = TELNET_STARTING_PORT
    list_of_vms = conf_yaml["vms"]
    devices = {}
    
    #Creating vm dictionary called "devices" one by one 
    for vm in list_of_vms:
        vm_config_file = vm['name'] + '.conf'
        
        #Getting config of device from zip archive
        try:
            with ZipFile(config_archive_location, 'r') as lazy_archive:
                vm_config = lazy_archive.read(vm_config_file).decode("utf-8")
        except Exception as err:
            vm_config = None
        
        cur_port += 1
        distribution = (vm['os'] + '_' + str(vm['version']))
        
        #Creating objects base on its OS
        if (distribution) == 'juniper_vmx_14':
            devices[lab_name + '_' + vm['name']] = JuniperVMX14ManageAll(lab_name = lab_name, vm = vm, port = cur_port, vm_config = vm_config)
        elif (distribution) == 'cisco_iosxr_15':
            devices[lab_name + '_' + vm['name']] = CiscoIOSXR15ManageAll(lab_name = lab_name, vm = vm, port = cur_port, vm_config = vm_config)
    return(devices)


def deploy_lab(config_archive_location):
    # Create dictionary of managment objects using function
    print('Deploying lab')
    devices = create_device_dict_with_archive(config_archive_location)
    #Deploying step by step. Methods of managment object is actually self explanitory.
    for device in devices:
        devices[device].create_net()
        devices[device].clone_volume()
        devices[device].create_vm()
        devices[device].waiting()
        devices[device].configure_vm()
    return(0)
    

def delete_lab(config_archive_location):
    # Deleting vms obviosly
    print('Deleting lab')
    devices = create_device_dict_with_archive(config_archive_location)
    for device in devices:
        devices[device].destroy_vm()
        devices[device].delete_volume()
    return(0)


#Working on this
#def save_lab(config_archive_location)
#        # Save configs
#        print('savings lab')
#        for device in devices:
#            devices[device].save_config_vm()

