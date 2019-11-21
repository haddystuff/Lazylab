import yaml
from lazylab.juniper.juniper_vmx_14_manage_all import JuniperVMX14ManageAll
from lazylab.juniper.juniper_vmxvcp_18_manage_all import JuniperVMXVCP18ManageAll
from lazylab.cisco.cisco_iosxr_15_manage_all import CiscoIOSXR15ManageAll
from lazylab.config_parser import *
from zipfile import ZipFile
import os
from lazylab.downloader import download_template_image
from xml.etree import ElementTree
import libvirt
import logging
"""
This file contain business logic functions that called from UI 
"""


logger = logging.getLogger('lazylab.tasker')

def create_zip_from_string(archive_path, filename, string):
    """
    This function write new file from string to zip archive.
    """
    
    
    config_archive = ZipFile(archive_path, mode="a")
    config_archive.writestr(filename, string)
    config_archive.close() 
    return 0

def create_device_dict_with_vm_descritpions(lab_name, active_only=True):
    
    #Creat diveces dictionary
    devices = {}
    with libvirt.open('qemu:///system') as virt_conn:
        
        #Getting runned vms objects in loop
        for vm_libvirt_object in virt_conn.listAllDomains(int(active_only)): 
            
            #Getting xml of vm and root of that xml
            vm_xml_root = ElementTree.fromstring(vm_libvirt_object.XMLDesc(0)) 
            
            #Trying to get description
            try:
                vm_xml_description = next(vm_xml_root.iter('description'))
            except StopIteration:
                #going to the next element of loop if no description found
                continue
            
            #Getting text of description
            vm_text_description = vm_xml_description.text
            
            #Checking if vm is auto-generated
            if '#Auto-generated vm with lazylab' in vm_text_description: 
                
                # Loading discription in yaml format to lab_parameters variable
                lab_parameters = yaml.load(vm_text_description, 
                                           Loader=yaml.FullLoader)
                
                # Getting vm_parameters
                vm_parameters = lab_parameters.get('vm')
                
                #Generating device dictionary(need to change way of generating later)
                if lab_parameters['lab_name'] == lab_name:
                    distribution = (vm_parameters.get('os') + '_' + str(vm_parameters.get('version')))
                    if (distribution) == 'juniper_vmx_14':
                        devices[lab_name + '_' + vm_parameters['name']] = JuniperVMX14ManageAll(lab_name=lab_parameters['lab_name'], vm=vm_parameters)
                    elif (distribution) == 'cisco_iosxr_15':
                        devices[lab_name + '_' + vm_parameters['name']] = CiscoIOSXR15ManageAll(lab_name=lab_parameters['lab_name'], vm=vm_parameters)
                    elif (distribution) == 'juniper_vmxvcp_18':
                        devices[lab_name + '_' + vm_parameters['name']] = JuniperVMXVCP18ManageAll(lab_name=lab_parameters['lab_name'], vm=vm_parameters)
    return devices


def check_if_template_image_exist(distribution):
    print(distribution)
    volume_list = DISTRIBUTION_IMAGE.get(distribution)
    print(volume_list)
    for volume in volume_list:
        if os.path.isfile(TEMPLATE_VOLUME_POOL_DIRECTORY + volume):
            return 0
        else:
            print('No ' + distribution + ' image\nDownloading...')
            download_template_image(distribution)
    return 0


def yaml_validate(conf_yaml):
    """
    This function check if yaml file has right structure
    """
    #Getting list of vms.
    vms_parameters_list = conf_yaml.get("vms")
    
    #Check if vms is actualy existing
    if vms_parameters_list == None:
        print("No \"vms\" block in config file")
        exit(1)
    
    #Check if lab name existing
    if conf_yaml.get('lab_name') == None:
        print("No \"lab_name\" block in config file")
        exit(1)
    
    #Check vm one by one.
    for vm_parameters in vms_parameters_list:
        #Check if name of vm is actially exist
        if vm_parameters.get('name') == None:
            print("No \"VM Name\" block in config file")
            exit(1)
        
        #Check if vm has right os and version(distibution in this context)
        distribution = vm_parameters.get('os') + '_' + str(vm_parameters.get('version'))
        
        if not(distribution in POSSIBLE_OS_LIST):
            print('Yaml file has bad syntax: wrong os name')
            exit(1)
        
        #Check if image of os exist on local disk
        check_if_template_image_exist(distribution)
    return 0


def create_device_dict_with_archive(config_archive_location):
    """
    This function creating dict of manage objects from zip archive. 
    It actially looks like this:
    { Testlab_router1: CiscoIOSXR15ManageAll_object
      Testlab_router2: JuniperVMX14ManageAll_object
    }
    """
    
    
    # Opening config file in zip archive, parsing with yaml and sending to
    # conf_yaml valiable
    with ZipFile(config_archive_location, 'r') as lazy_archive:
        conf_yaml = yaml.load(lazy_archive.read(CONFIG_FILE_NAME), 
                              Loader=yaml.FullLoader)
    
    #Validating syntax and more of conf_yaml
    yaml_validate(conf_yaml)
    
    #Setting some valiables
    lab_name = conf_yaml.get("lab_name")
    cur_port = TELNET_STARTING_PORT
    vms_parameters_list = conf_yaml.get("vms")
    devices = {}
    
    #Creating vm dictionary called "devices" one by one 
    for vm_parameters in vms_parameters_list:
        vm_config_file = vm_parameters.get('name') + '.conf'
        
        #Getting config of device from zip archive
        try:
            with ZipFile(config_archive_location, 'r') as lazy_archive:
                vm_config = lazy_archive.read(vm_config_file).decode("utf-8")
        except Exception as err:
            vm_config = None
        
        cur_port += 1
        distribution = (vm_parameters.get('os') + '_' + str(vm_parameters.get('version')))
        
        #Creating objects base on its OS
        # need to change way of generating later
        if (distribution) == 'juniper_vmx_14':
            devices[lab_name + '_' + vm_parameters['name']] = JuniperVMX14ManageAll(lab_name=lab_name, vm=vm_parameters, port=cur_port, vm_config=vm_config)
        elif (distribution) == 'cisco_iosxr_15':
            devices[lab_name + '_' + vm_parameters['name']] = CiscoIOSXR15ManageAll(lab_name=lab_name, vm=vm_parameters, port=cur_port, vm_config=vm_config)
        elif (distribution) == 'juniper_vmxvcp_18':
            devices[lab_name + '_' + vm_parameters['name']] = JuniperVMXVCP18ManageAll(lab_name=lab_name, vm=vm_parameters, port=cur_port, vm_config=vm_config)
    return devices


def deploy_lab(config_archive_location):
    
    logging.debug('deploying lab')

    # Create dictionary of managment objects using function
    devices = create_device_dict_with_archive(config_archive_location)
    
    #Deploying step by step. Methods of managment object is actually 
    #self explanitory.
    for device in devices:
        devices[device].create_net()
        devices[device].clone_volume()
        devices[device].create_vm()
        devices[device].waiting()
        devices[device].configure_vm()
    return 0


def delete_lab(lab_name):
    """
    Deleting vms obviosly
    """
    logging.info('deleting lab')
    
    # generating device dictionary
    devices = create_device_dict_with_vm_descritpions(lab_name, 
                                                      active_only=False)

    # Deleteing vms in dictionary
    for device in devices:
        devices[device].destroy_vm()
        devices[device].delete_volume()
    return 0


def save_lab(old_lab_name, new_lab_name):
        """ 
        Save configs
        Works bad sometimes need to work on this more
        """
        logging.debug('savings lab')

        # Creating config_dictionary
        config_dictionary = {}
        config_dictionary['lab_name'] = new_lab_name
        config_dictionary['vms'] = []
        
        # Creating device dictionary
        devices = create_device_dict_with_vm_descritpions(old_lab_name)
        
        # Ctarting iteration using devices dictionary 
        for device in devices:
            
            # Find out network connections
            devices[device].get_vm_networks()
            
            # Adding device parameters to config_dictionary 
            config_dictionary['vms'].append(devices[device].vm)
            
            # Find out vm config
            devices[device].get_config_vm()
            
            # Getting vm_config to dev_config_str and sending it to archive
            dev_config_str = devices[device].vm_config
            create_zip_from_string(f"{PATH_TO_MODULE}/labs/{new_lab_name}.lazy",
                                   f"{devices[device].vm_short_name}.conf",
                                   dev_config_str)
            
        # converting config_dictionary to yaml string and sending it to archive
        config_str = yaml.dump(config_dictionary)
        create_zip_from_string(f"{PATH_TO_MODULE}/labs/{new_lab_name}.lazy",
                               "config.yml", config_str)
        return 0
