import unittest
from lazylab.config_parser import *
from lazylab.base.base_manage_vm import BaseManageVM
from lazylab.constants import PATH_TO_MODULE, TEMPLATE_IMAGE_LIST
from xml.etree import ElementTree
import libvirt
import os.path

TEST_VM_PARAMETERS = {'juniper_vmx_14': {'name': 'Tested_VM', 
                                        'os': 'juniper_vmx',
                                        'version': 14, 
                                        'interfaces': {'ge-0/0/0': 'Unknown_net'}},
                      'juniper_vmxvcp_17': {'name': 'Tested_VM', 
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

        for distribution, vm_parameters in TEST_VM_PARAMETERS.items():
            class_name = vm_parameters.get('os') + str(vm_parameters.get('version')) + 'ManageAll'
            DeviceClass = type(class_name, class_parents_tuple, {})
            self.devices[distribution] = DeviceClass(lab_name=lab_name, vm_parameters=vm_parameters)
        
    def test_clone_delte_volume(self):
        
        for distribution in self.devices:
            device = self.devices[distribution]
            device.clone_volume()
            
            template_volume_list = TEMPLATE_IMAGE_LIST.get(device.distribution)
            for template_volume_name in template_volume_list:
                with libvirt.open('qemu:///system') as conn: 
                    volume_pool = conn.storagePoolLookupByName(VOLUME_POOL_NAME)
                    volume_pool_xml_root = ElementTree.fromstring(volume_pool.XMLDesc())
                    target = next(volume_pool_xml_root.iter('target'))
                    volume_pool_path = next(target.iter('path')).text
                    clone_to_path = volume_pool_path + '/' + device.vm_name + template_volume_name
                with self.subTest(action='clone', distribution=distribution):
                    self.assertTrue(os.path.exists(clone_to_path))
                
            device.delete_volume()
            with self.subTest(action='delete', distribution=distribution):
                self.assertTrue(not (os.path.exists(clone_to_path)))
