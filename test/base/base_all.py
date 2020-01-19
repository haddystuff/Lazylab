import unittest
from lazylab.config_parser import *
from lazylab.base.base_manage_vm import BaseManageVM
from lazylab.constants import PATH_TO_MODULE, TEMPLATE_IMAGE_LIST
from xml.etree import ElementTree
import libvirt
import os.path

class BaseAll(unittest.TestCase):
    def setUp(self):
        """
        Creating class and object to work with
        """
        class_parents_tuple = (BaseManageVM,)
        lab_name = 'Test_Lab'
        vm_parameters = {'name': 'Tested_VM', 
                         'os': 'juniper_vmx',
                         'version': 14, 
                         'interfaces': {'ge-0/0/0': 'Unknown_net'}}
        DeviceClass = type('JuniperVMX14ManageAll', class_parents_tuple, {})
        self.device = DeviceClass(lab_name=lab_name, vm_parameters=vm_parameters)
        self.clone_to_path = None
        
    def test_clone_delte_volume(self):
        self.device.clone_volume()
        clone_from_path = f'{PATH_TO_MODULE}/images/juniper_vmx_14_template.qcow2'
        
        template_volume_list = TEMPLATE_IMAGE_LIST.get(self.device.distribution)
        for template_volume_name in template_volume_list:
            with libvirt.open('qemu:///system') as conn: 
                volume_pool = conn.storagePoolLookupByName(VOLUME_POOL_NAME)
                volume_pool_xml_root = ElementTree.fromstring(volume_pool.XMLDesc())
                target = next(volume_pool_xml_root.iter('target'))
                volume_pool_path = next(target.iter('path')).text
                clone_to_path = volume_pool_path + '/' + self.device.vm_name + template_volume_name
            with self.subTest(action='clone'):
                self.assertTrue(os.path.exists(clone_to_path))
            
        self.device.delete_volume()
        with self.subTest(action='delete'):
            self.assertTrue(not (os.path.exists(clone_to_path)))
