"""Tasker Class"""
from lazylab.constants import LAB_CONFIG_PATH
from lazylab.tasker.dictionary_creator.dictionary_creator import DictionaryCreator
from lazylab.tasker.zipper import *
from lazylab.tasker.exceptions import *
from lazylab.tasker.yaml_parser import parse_yaml
from lazylab.tasker.downloader.downloader import check_images, download_lab_config_file
import logging


logger = logging.getLogger(__name__)

class Tasker():
    """Tasker Class"""
    def __init__(self, **kvargs):
        """
        This is business rules class.
        All methods of this class should be called from UI.
        """
        
        # Saving arguments
        self.vms_attributes = kvargs


    def deploy_lab(self, lab_name):
        """
        Deploying lab
        """
        
        logger.info('deploying lab')
        
        # Unzip lab arhive to get configs of lab and devices
        try:
            conf_yaml, vm_configs = unzip_lab(lab_name)
            
        # If there is no archive the download it
        except NoLabArchive:
            
            logger.warning('No lab archive in local storage')
            download_lab_config_file(lab_name)
        
        # Validating syntax of conf_yaml    
        conf_dict = parse_yaml(conf_yaml)
            
        # Checking if requested in conf_yaml file images exist
        check_images(conf_dict)
        
        # Create dictionary of managment objects
        device_dict_creator = DictionaryCreator(**self.vms_attributes)
        devices = device_dict_creator.create_device_dict_with_archive(conf_dict, vm_configs)
        
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
        device_dict_creator = DictionaryCreator(**self.vms_attributes)
        devices = device_dict_creator.create_device_dict_with_vm_description(lab_name, 
                                                                    active_only=False)

        # Deleteing vms in dictionary
        for device_name, device in devices.items():
            
            device.destroy_vm()
            
        return 0


    def save_lab(self, old_lab_name, new_lab_name, saved_lab_path = LAB_CONFIG_PATH):
        """ 
        Save configs
        needed some refactoring
        """
        
        logger.debug('savings lab')
        
        # Setting archive path
        new_lab_archive_path = f'{saved_lab_path}{new_lab_name}.lazy'

        # Creating new lab config_dictionary
        conf_dict = {}
        conf_dict['lab_name'] = new_lab_name
        conf_dict['vms'] = []
        vm_configs = {}
        # Creating device dictionary
        device_dict_creator = DictionaryCreator(**self.vms_attributes)
        devices = device_dict_creator.create_device_dict_with_vm_description(old_lab_name)
        
        # Starting iteration using devices dictionary 
        # Saving lab step by step. Methods is actually self
        # explanitory.
        for device_name, device in devices.items():
            
            # Find out network connections
            device.get_vm_networks()
            
            # Adding device parameters to config_dictionary 
            conf_dict['vms'].append(device.vm_parameters)
            
            # Getting vm config
            device.get_vm_config()
            
            # Getting short name
            device_short_name = device.vm_short_name
            
            # Getting vm_config to dev_config_str and sending it to archive
            vm_configs[device_short_name] = device.vm_config
        
        zip_to_archive(conf_dict, vm_configs, new_lab_archive_path)
                                    
        return 0
