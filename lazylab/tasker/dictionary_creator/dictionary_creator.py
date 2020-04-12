"""Dictionary creator module"""
from lazylab.cisco.cisco_iosxr_manage_config import CiscoIOSXRManageConfig
from lazylab.juniper.juniper_vmxvcp_manage_config import JuniperVMXVCPManageConfig
from lazylab.juniper.juniper_vmx_manage_config import JuniperVMXManageConfig
from lazylab.tasker.tasker_constants import OS_TO_CLASS, OS_TO_CLASS_NAME
from lazylab.tasker.tasker_constants import LAB_ATTRIBUTE_TO_CLASS
from lazylab.tasker.tasker_helpers import is_port_in_use
from lazylab.base.base_manage_vm import BaseManageVM
from lazylab.constants import DEVICE_DESCRIPTION_MAIN_STR
from lazylab.config_parser import *
from lazylab.tasker.downloader.downloader import download_lab_config_file
from xml.etree import ElementTree
import libvirt
import logging
import yaml

logger = logging.getLogger(__name__)

class DictionaryCreator():
    """
    This class create dictionary of device objects which then use to control
    vms and configs. Also there is create_device function which is fabric.
    : param volume_format: (str) volume format(qcow2 only supported for now)
    : param vm_type: (str) virtual machine type(persistent or not)
    """
    def __init__(self, **kvargs):
        # Creating generic attributes list
        self.generic_vms_attributes = []
        
        # Creating managers class list - which is place where already created
        # classes will be stored. 
        self.managers_classes = {}
        
        # Unpacking
        self.volume_format = kvargs.get('volume_format', 'qcow')
        self.vm_type = kvargs.get('vm_type', 'persistent')
        
        # Filling generic attributes
        self.generic_vms_attributes.append(self.volume_format)
        self.generic_vms_attributes.append(self.vm_type)
        
    def create_device_dict_with_archive(self, conf_dict, vm_configs):
        """
        This method creates dict of manage objects from zip archive. 
        It actially looks like this:
        { Testlab_router1: CiscoIOSXR5ManageAll_object
          Testlab_router2: JuniperVMX14ManageAll_object
        }
        """
        
        # Setting vm and lab parameters
        lab_name = conf_dict.get('lab_name')
        cur_port = TELNET_STARTING_PORT
        vms_parameters_list = conf_dict.get('vms')
        devices = {}
        
        # Creating vm dictionary called "devices" one by one 
        for vm_parameters in vms_parameters_list:
            
            # Unpacking parameters
            vm_name = vm_parameters.get('name')
            vm_config_file_name = vm_name + '.conf'
            
            vm_config = vm_configs.get(vm_config_file_name, None)
            
            # Take next port to use as telnet console if it isn't in use
            cur_port += 1
            while(is_port_in_use(cur_port)):
                cur_port += 1
            
            # Creating device dict
            devices[f'{lab_name}_{vm_name}'] = self.create_device(lab_name=lab_name, 
                                                           vm_parameters=vm_parameters,
                                                           port=cur_port, 
                                                           vm_config=vm_config)
                                                           
        return devices
        
    def create_device_dict_with_vm_description(self, lab_name, active_only=True):
        """
        This method create device dictionary from vm descriptions that we
        created earlier. Also users can create it by hand.
        It actially looks like this:
        { Testlab_router1: CiscoIOSXR5ManageAll_object
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
                    
                    # Loading discription in yaml format to lab_parameters
                    # variable
                    vm_description_dict = yaml.load(vm_text_description, 
                                               Loader=yaml.FullLoader)
                    
                    if vm_description_dict['lab_name'] == lab_name:
                    
                        # Getting vm_parameters
                        vm_parameters = vm_description_dict.get('vm')
                        
                        # Getting vm_name
                        vm_name = vm_parameters.get('name')
                        
                        # Creating device dictionary
                        devices[f'{lab_name}_{vm_name}'] = self.create_device(lab_name=lab_name, 
                                                               vm_parameters=vm_parameters)
        
        return devices
        
        

    def create_device(self, **kvargs):
        """
        This is device object generator, wich is just small Fabric.
        """
        
        lab_name = kvargs.get('lab_name') 
        vm_parameters = kvargs.get('vm_parameters')
        port = kvargs.get('port')
        vm_config = kvargs.get('vm_config')
        os = vm_parameters.get('os')
        version = str(vm_parameters.get('version'))
        
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
            logger.info('Creating new class called {class_name} with parents {class_parents_tuple}')
            DeviceClass = type(class_name, class_parents_tuple, {})
            
            # Add new class to managers_classes dictionary
            self.managers_classes[class_name] = DeviceClass
        
        return DeviceClass(lab_name=lab_name, 
                           vm_parameters=vm_parameters,
                           port=port, 
                           vm_config=vm_config)
