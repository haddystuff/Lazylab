"""Tasker Class"""
from lazylab.constants import DEVICE_DESCRIPTION_MAIN_STR, LAB_CONFIG_PATH
from lazylab.tasker.device_class_generator.device_class_generator import DeviceClassGenerator
from lazylab.config_parser import *
from lazylab.tasker.tasker_helpers import *
from zipfile import ZipFile
from lazylab.downloader import download_lab_config_file
from xml.etree import ElementTree
import libvirt
import logging
import yaml


logger = logging.getLogger(__name__)

class Tasker():
    """Tasker Class"""
    def __init__(self, **kvargs):
        """
        This is business logic class.
        All methods of this class should be called from UI.
        """
        
        # Saving arguments
        self.vms_attributes = kvargs
        

    def create_device_dict_with_vm_description(self, lab_name, active_only=True):
        """
        This method create device dictionary from vm descriptions that we
        created earlier. Also users can create it by hand.
        It actially looks like this:
        { Testlab_router1: CiscoIOSXR15ManageAll_object
          Testlab_router2: JuniperVMX14ManageAll_object
        }
        """
        
        # Create devices dictionary
        devices = {}
        
        with libvirt.open('qemu:///system') as virt_conn:
            
            # Getting runned vms objects in loop
            for vm_libvirt_object in virt_conn.listAllDomains(int(active_only)): 
                
                # Getting xml of vm and root of that xml
                vm_xml_root = ElementTree.fromstring(vm_libvirt_object.XMLDesc(0)) 
                
                # Trying to get description
                try:
                    
                    vm_xml_description = next(vm_xml_root.iter('description'))
                    
                except StopIteration:
                    
                    # Going to the next element of loop if no description found
                    continue
                
                # Getting text of description
                vm_text_description = vm_xml_description.text
                
                # Checking if vm is auto-generated
                if DEVICE_DESCRIPTION_MAIN_STR in vm_text_description: 
                    
                    # Loading discription in yaml format to lab_parameters variable
                    vm_description_dict = yaml.load(vm_text_description, 
                                               Loader=yaml.FullLoader)
                    
                    # Getting vm_parameters
                    vm_parameters = vm_description_dict.get('vm')
                    
                    # Generating device dictionary(need to change way of generating later)
                    if vm_description_dict['lab_name'] == lab_name:
                        generator = DeviceClassGenerator(**self.vms_attributes)
                        DeviceClass = generator.generate_class(os=vm_parameters.get('os'), version=vm_parameters.get('version'))
                        devices[lab_name + '_' + vm_parameters.get('name')] = DeviceClass(lab_name=lab_name, vm_parameters=vm_parameters)
        
        return devices


    def create_device_dict_with_archive(self, config_archive_name):
        """
        This function creating dict of manage objects from zip archive. 
        It actially looks like this:
        { Testlab_router1: CiscoIOSXR15ManageAll_object
          Testlab_router2: JuniperVMX14ManageAll_object
        }
        """
        
        # Getting config_archive_location
        config_archive_location = LAB_CONFIG_PATH + config_archive_name
        
        # Opening config file in zip archive, parsing with yaml and sending to
        # conf_yaml valiable
        try:
            
            with ZipFile(config_archive_location, 'r') as lazy_archive:
                conf_yaml = yaml.load(lazy_archive.read(CONFIG_FILE_NAME), 
                                      Loader=yaml.FullLoader)
                                      
        except FileNotFoundError as err:
            
            logger.info(f'{config_archive_location} not found, trying to download from server')
            
            # Downloading .lazy archive from server
            download_lab_config_file(config_archive_name)
        
        # Validating syntax and more of conf_yaml
        yaml_validate(conf_yaml)
        
        # Setting vm and lab parameters
        lab_name = conf_yaml.get('lab_name')
        cur_port = TELNET_STARTING_PORT
        vms_parameters_list = conf_yaml.get('vms')
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
                    vm_config = lazy_archive.read(vm_config_file).decode('utf-8')
                    
            except KeyError as err:
                
                logger.warning(f'{err}')
                
                vm_config = None
            
            #Take next port to use as telnet console if it isn't in use
            cur_port += 1
            while(is_port_in_use(cur_port)):
                cur_port += 1
            
            #Creating objects base on its OS
            generator = DeviceClassGenerator(**self.vms_attributes)
            DeviceClass = generator.generate_class(os=os, version=version)
            devices[f'{lab_name}_{vm_name}'] = DeviceClass(lab_name=lab_name, 
                                                           vm_parameters=vm_parameters,
                                                           port=cur_port, 
                                                           vm_config=vm_config)
        return devices


    def deploy_lab(self, lab_name):
        """
        This method run throgh all small methods that helps to deploy lab
        """
        
        logger.info('deploying lab')
        
        config_archive_name = f'{lab_name}.lazy'
        
        # Create dictionary of managment objects using function
        devices = self.create_device_dict_with_archive(config_archive_name)
        
        # Deploying every device step by step. Methods is actually self
        # explanitory.
        for device_name, device in devices.items():
            
            device.create_net()
            device.create_vm()
            device.waiting()
            device.configure_vm()
            
        return 0


    def delete_lab(self, lab_name):
        """
        Deleting vms
        """
        
        logger.info('deleting lab')
        
        # generating device dictionary
        devices = self.create_device_dict_with_vm_description(lab_name, 
                                                             active_only=False)

        # Deleteing vms in dictionary
        for device_name, device in devices.items():
            
            device.destroy_vm()
            
        return 0


    def save_lab(self, old_lab_name, new_lab_name, saved_lab_path = LAB_CONFIG_PATH):
        """ 
        Save configs
        Works bad sometimesl. need to work on this more
        """
        
        logger.debug('savings lab')
        
        # Setting archive path
        new_lab_archive_path = f'{saved_lab_path}{new_lab_name}.lazy'

        # Creating config_dictionary
        config_dictionary = {}
        config_dictionary['lab_name'] = new_lab_name
        config_dictionary['vms'] = []
        
        # Creating device dictionary
        devices = self.create_device_dict_with_vm_description(old_lab_name)
        
        # Ctarting iteration using devices dictionary 
        for device_name, device in devices.items():
            
            # Find out network connections
            device.get_vm_networks()
            
            # Adding device parameters to config_dictionary 
            config_dictionary['vms'].append(device.vm_parameters)
            
            # Find out vm config
            device.get_vm_config()
            
            # Getting vm_config to dev_config_str and sending it to archive
            dev_config_str = device.vm_config
            device_config_filename = f'{device.vm_short_name}.conf'
            
            create_zip_from_string(new_lab_archive_path,
                                   device_config_filename,
                                   dev_config_str)
            
        # Converting config_dictionary to yaml string and sending it to archive
        config_str = yaml.dump(config_dictionary)
        create_zip_from_string(new_lab_archive_path, 'config.yml', config_str)
                                    
        return 0
