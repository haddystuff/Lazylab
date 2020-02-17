"""Device Creator Class"""
from lazylab.cisco.cisco_iosxr_manage_config import CiscoIOSXRManageConfig
from lazylab.juniper.juniper_vmxvcp_manage_config import JuniperVMXVCPManageConfig
from lazylab.juniper.juniper_vmx_manage_config import JuniperVMXManageConfig
from lazylab.tasker.tasker_constants import OS_TO_CLASS
from lazylab.tasker.tasker_constants import OS_TO_CLASS_NAME
from lazylab.tasker.tasker_constants import LAB_ATTRIBUTE_TO_CLASS
from lazylab.base.base_manage_vm import BaseManageVM
import logging


logger = logging.getLogger(__name__)

class DeviceCreator():
    """Device Class Generator Class"""
    def __init__(self, **kvargs):
        """
        This class is small Factory, but without object creating.
        This class is used only by Tasker module, wich should create object by 
        himself.
        :param volume_format(str): format of volumes in pool. Possible values
        are 'qcow' for now, but in future we will implement 'LVM' and 'LUN'.
        :param vm_type(str): persistentcy of vm. Possible values are 
        'persistent', but in future we will implement 'transient'.
        """
        
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

        
    def create_device(self, **kvargs):
        """
        This is class generator, wich is just small Fabric, but without object
        creating.
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
