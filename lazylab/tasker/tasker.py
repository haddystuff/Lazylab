"""Tasker Class"""
from lazylab.cisco.cisco_iosxr_manage_config import CiscoIOSXRManageConfig
from lazylab.juniper.juniper_vmxvcp_manage_config import JuniperVMXVCPManageConfig
from lazylab.juniper.juniper_vmx_manage_config import JuniperVMXManageConfig
from lazylab.tasker.tasker_constants import OS_TO_CLASS
from lazylab.tasker.tasker_constants import OS_TO_CLASS_NAME
from lazylab.tasker.tasker_constants import LAB_ATTRIBUTE_TO_CLASS
from lazylab.constants import POSSIBLE_OS_LIST, DEVICE_DESRIPTION_MAIN_STR
from lazylab.base.base_manage_vm import BaseManageVM
from lazylab.config_parser import *
from lazylab.constants import TEMPLATE_IMAGE_LIST
from lazylab.tasker.tasker_helpers import is_port_in_use
from zipfile import ZipFile
from lazylab.downloader import download_template_image
from lazylab.downloader import download_lab_config_file
from xml.etree import ElementTree
import libvirt
import logging
import os
import yaml


logger = logging.getLogger('lazylab.tasker.tasker')

class Tasker():
    """Tasker Class"""
    def __init__(self, **kvargs):
        """
        This class combine dynamic manager class creation and business logic.
        All methods of this class should be called from UI.
        :param volume_format(str): format of volumes in pool. Possible values
        are 'qcow' for now, but in future we will implement 'LVM' and 'LUN'.
        :param vm_type(str): persistentcy of vm. Possible values are 
        'persistent', but in future we will implement 'transient'.
        """
        
        # Creating generic attributes list
        self.generic_vms_attributes = []
        
        # Creating managers class list - which is place where already created classes
        # will be stored. 
        self.managers_classes = {}
        
        # Unpacking
        self.volume_format = kvargs.get('volume_format', 'qcow')
        self.vm_type = kvargs.get('vm_type', 'persistent')
        
        # Filling generic attributes
        self.generic_vms_attributes.append(self.volume_format)
        self.generic_vms_attributes.append(self.vm_type)
        
    def device_class_generator(self, **kvargs):
        """This is class generator, wich is just small fabric."""
        
        #Unpacking arguments
        os = kvargs.get('os')
        version = str(kvargs.get('version'))
        
        # Setting full class name
        class_name = OS_TO_CLASS_NAME.get(os) + version + 'ManageAll'
        
        try:
            
            # Get class from managers_classes dict. If there is no class then
            # create it
            DeviceClass = self.managers_classes[class_name]
        
        except KeyError:
        
            # Getting config class from OS_TO_CLASS dict
            config_class = OS_TO_CLASS.get(os)
            
            # Setting first class in class parents list
            class_parents_list = [config_class]
            
            # Adding new parents to class parents list depend of a generic 
            # attributes of lab
            for attribute in  self.generic_vms_attributes:
                class_parents_list.append(LAB_ATTRIBUTE_TO_CLASS.get(attribute))
            
            # Add BaseManageVM to parents list
            class_parents_list.append(BaseManageVM)
                
            # Convert class parents list to tuple
            class_parents_tuple = tuple(class_parents_list)
            
            # Creating device class
            logging.info('Creating new class called {class_name} with parents {class_parents_tuple}')
            DeviceClass = type(class_name, class_parents_tuple, {})
            
            # Add new class to managers_classes dictionary
            self.managers_classes[class_name] = DeviceClass
        
        return DeviceClass
        
    def create_zip_from_string(self, archive_path, filename, string):
        """This method write new file from string to zip archive."""
        
        config_archive = ZipFile(archive_path, mode="a")
        config_archive.writestr(filename, string)
        config_archive.close() 
        
        return 0

    def create_device_dict_with_vm_descritpions(self, lab_name, active_only=True):
        """
        This method create device dictionary from vm descriptions that we
        created earlier. Also users can create it by hand.
        It actially looks like this:
        { Testlab_router1: CiscoIOSXR15ManageAll_object
          Testlab_router2: JuniperVMX14ManageAll_object
        }
        """
        
        #Create devices dictionary
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
                if DEVICE_DESRIPTION_MAIN_STR in vm_text_description: 
                    
                    # Loading discription in yaml format to lab_parameters variable
                    vm_description_dict = yaml.load(vm_text_description, 
                                               Loader=yaml.FullLoader)
                    
                    # Getting vm_parameters
                    vm_parameters = vm_description_dict.get('vm')
                    
                    #Generating device dictionary(need to change way of generating later)
                    if vm_description_dict['lab_name'] == lab_name:
                        DeviceClass = self.device_class_generator(os=vm_parameters.get('os'), version=vm_parameters.get('version'))
                        devices[lab_name + '_' + vm_parameters['name']] = DeviceClass(lab_name=lab_name, vm_parameters=vm_parameters)
        
        return devices


    def check_if_template_images_exist(self, distribution):
        """
        This method check if template images exist, if not it running 
        download_template_image function wich download image.
        """
        
        logging.info('checking if {distribution} template image exist')
        
        # Getting volume base on distribution
        volume_list = TEMPLATE_IMAGE_LIST.get(distribution)
        
        logging.info('we need this images: {volume_list}')
        
        # Iterating through volume list
        for template_volume_name in volume_list:
            
            # checking file existence
            if os.path.isfile(TEMPLATE_VOLUME_POOL_DIRECTORY + template_volume_name):
                
                logging.info('{template_volume_name} image exist')
                
            else:
                
                logging.info('{template_volume_name} image dont exist')
                print('No ' + distribution + ' image\nDownloading...')
                
                # downloading image
                download_template_image(template_volume_name)
                
        return 0


    def yaml_validate(self, conf_yaml):
        """
        This function check if yaml file has right structure and syntax.
        We need to modify this code so we can check all syntax in yaml file.
        """
        
        #Getting list of vms.
        vms_parameters_list = conf_yaml.get("vms")
        
        #Check if vms is actualy existing
        if vms_parameters_list is None:
            print("No \"vms\" block in config file")
            exit(1)
        
        #Check if lab name existing
        if conf_yaml.get('lab_name') is None:
            print("No \"lab_name\" block in config file")
            exit(1)
        
        #Check vm one by one.
        for vm_parameters in vms_parameters_list:
            
            #Check if name of vm is actially exist
            if vm_parameters.get('name') is None:
                print("No \"VM Name\" block in config file")
                exit(1)
            
            #Check if vm has right os and version(distibution in this context)
            distribution = vm_parameters.get('os') + '_' + str(vm_parameters.get('version'))
            
            if not(distribution in POSSIBLE_OS_LIST):
                print('Yaml file has bad syntax: wrong os name')
                exit(1)
            
            #Check if image of os exist on local disk
            self.check_if_template_images_exist(distribution)
            
        return 0


    def create_device_dict_with_archive(self, config_archive_name):
        """
        This function creating dict of manage objects from zip archive. 
        It actially looks like this:
        { Testlab_router1: CiscoIOSXR15ManageAll_object
          Testlab_router2: JuniperVMX14ManageAll_object
        }
        """
        
        # gettign config_archive_location
        config_archive_location = LAB_CONFIG_PATH + config_archive_name
        
        # Opening config file in zip archive, parsing with yaml and sending to
        # conf_yaml valiable
        try:
            
            with ZipFile(config_archive_location, 'r') as lazy_archive:
                conf_yaml = yaml.load(lazy_archive.read(CONFIG_FILE_NAME), 
                                      Loader=yaml.FullLoader)
                                      
        except FileNotFoundError as err:
            
            logging.info(f'{config_archive_location} not found, trying to download from server')
            
            # Downloading .lazy archive from server
            download_lab_config_file(config_archive_name)
        
        # Validating syntax and more of conf_yaml
        self.yaml_validate(conf_yaml)
        
        # Setting vm and lab parameters
        lab_name = conf_yaml.get("lab_name")
        cur_port = TELNET_STARTING_PORT
        vms_parameters_list = conf_yaml.get("vms")
        devices = {}
        
        # Creating vm dictionary called "devices" one by one 
        for vm_parameters in vms_parameters_list:
            
            # Unpacking parameters
            vm_config_file = vm_parameters.get('name') + '.conf'
            os = vm_parameters.get('os')
            version = str(vm_parameters.get('version'))
            vm_name = vm_parameters.get('name')
            
            # Getting config of device from zip archive
            try:
                
                # Opening .lazy file
                with ZipFile(config_archive_location, 'r') as lazy_archive:
                    
                    # Decoding from utf-8
                    vm_config = lazy_archive.read(vm_config_file).decode("utf-8")
                    
            except KeyError as err:
                
                logging.info(f'{err}')
                
                vm_config = None
            
            #Take next port to use as telnet console if it isn't in use
            cur_port += 1
            while(is_port_in_use(cur_port)):
                cur_port += 1
            
            #Creating objects base on its OS
            DeviceClass = self.device_class_generator(os=os, version=version)
            devices[lab_name + '_' + vm_name] = DeviceClass(lab_name=lab_name, vm_parameters=vm_parameters, port=cur_port, vm_config=vm_config)
        
        return devices


    def deploy_lab(self, lab_name):
        """
        This method run throgh all small method that helps to deploy lab
        """
        
        logging.info('deploying lab')
        config_archive_name = f'{lab_name}.lazy'
        # Create dictionary of managment objects using function
        devices = self.create_device_dict_with_archive(config_archive_name)
        
        # Deploying every device step by step. Methods is actually self
        # explanitory.
        for device in devices:
            devices[device].create_net()
            devices[device].create_vm()
            devices[device].waiting()
            devices[device].configure_vm()
        return 0


    def delete_lab(self, lab_name):
        """
        Deleting vms obviosly
        """
        
        logging.info('deleting lab')
        
        # generating device dictionary
        devices = self.create_device_dict_with_vm_descritpions(lab_name, 
                                                          active_only=False)

        # Deleteing vms in dictionary
        for device in devices:
            devices[device].destroy_vm()
        return 0


    def save_lab(self, old_lab_name, new_lab_name):
        """ 
        Save configs
        Works bad sometimesl. need to work on this more
        """
        logging.debug('savings lab')
        # Setting valiables
        new_lab_archive_path = f"{LAB_CONFIG_PATH}{new_lab_name}.lazy"

        # Creating config_dictionary
        config_dictionary = {}
        config_dictionary['lab_name'] = new_lab_name
        config_dictionary['vms'] = []
        
        # Creating device dictionary
        devices = self.create_device_dict_with_vm_descritpions(old_lab_name)
        
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
            device_config_filename = f"{devices[device].vm_short_name}.conf"
            
            self.create_zip_from_string(new_lab_archive_path,
                                        device_config_filename,
                                        dev_config_str)
            
        # converting config_dictionary to yaml string and sending it to archive
        config_str = yaml.dump(config_dictionary)
        self.create_zip_from_string(new_lab_archive_path, "config.yml",
                                    config_str)
                                    
        return 0
