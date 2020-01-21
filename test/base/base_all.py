import unittest
from lazylab.config_parser import *
from lazylab.base.base_manage_vm import BaseManageVM
from lazylab.constants import PATH_TO_MODULE, TEMPLATE_IMAGE_LIST
from xml.etree import ElementTree
from lazylab.tasker.tasker_helpers import is_port_in_use
import libvirt
import os.path

TEST_VM_PARAMETERS = {'juniper_vmx_14': {'name': 'Tested_VM_1', 
                                        'os': 'juniper_vmx',
                                        'version': 14, 
                                        'interfaces': {'ge-0/0/0': 'Unknown_net'}},
                      'juniper_vmxvcp_18': {'name': 'Tested_VM_2', 
                                           'os': 'juniper_vmxvcp',
                                           'version': 18, 
                                           'interfaces': {'ge-0/0/0': 'Unknown_net'}}}

class BaseAll(unittest.TestCase):
    def setUp(self):
        """
        Creating class and object to work with
        """
        self.devices = {}
        class_parents_tuple = (BaseManageVM,)
        lab_name = 'Test_Lab'
        cur_port = TELNET_STARTING_PORT

        for distribution, vm_parameters in TEST_VM_PARAMETERS.items():
            class_name = vm_parameters.get('os') + str(vm_parameters.get('version')) + 'ManageAll'
            DeviceClass = type(class_name, class_parents_tuple, {})
            cur_port += 1
            while(is_port_in_use(cur_port)):
                cur_port += 1
            self.devices[distribution] = DeviceClass(lab_name=lab_name, vm_parameters=vm_parameters, port=cur_port)
        
    def test_clone_delete_volume(self):
        
        for distribution, device in self.devices.items():
            print(f'cloning {distribution}')
            device.clone_volume()
            
            template_volume_list = TEMPLATE_IMAGE_LIST.get(device.distribution)
            for template_volume_name in template_volume_list:
                with libvirt.open('qemu:///system') as conn: 
                    volume_pool = conn.storagePoolLookupByName(VOLUME_POOL_NAME)
                    volume_pool_xml_root = ElementTree.fromstring(volume_pool.XMLDesc())
                    target = next(volume_pool_xml_root.iter('target'))
                    volume_pool_path = next(target.iter('path')).text
                    clone_to_path = f'{volume_pool_path}/{device.vm_name}_{template_volume_name}'
                with self.subTest(action='clone', distribution=distribution):
                    self.assertTrue(os.path.exists(clone_to_path))
                
            device.delete_volume()
            with self.subTest(action='delete', distribution=distribution):
                self.assertTrue(not (os.path.exists(clone_to_path)))
    
    def test_create_destroy_vm(self):
        for distribution, device in self.devices.items():
            
            # Testing create
            device.create_net()
            device.create_vm()
            with libvirt.open('qemu:///system') as conn:
                dom = conn.lookupByName(device.vm_name) 
                flag = bool(dom.isActive())
            with self.subTest(action='create', distribution=distribution):
                self.assertTrue(flag)
            
            # Testing get_vm_networks
            interfaces_we_get = device.vm_parameters['interfaces']
            interfaces_we_want_to_get = TEST_VM_PARAMETERS[distribution].get('interfaces')
            with self.subTest(action='get_vm_networks', distribution=distribution):
                self.assertTrue(bool(interfaces_we_get == interfaces_we_want_to_get))
            
            # Testing destroy
            flag = False
            device.destroy_vm()
            
            with libvirt.open('qemu:///system') as conn:
                try:
                    dom = conn.lookupByName(device.vm_name)
                except libvirt.libvirtError as err:
                    
                    # checking if libvirt error code is
                    # 42 - VIR_ERR_OPERATION_INVALID. If not - exit the script
                    flag = bool(err.get_error_code() == 42)
            
            with self.subTest(action='delete', distribution=distribution):
                self.assertTrue(flag)
                
            
            # Testing destroy second time
            with self.subTest(action='second_delete', distribution=distribution):
                self.assertTrue(device.destroy_vm() == 0)
        return(0)
        
