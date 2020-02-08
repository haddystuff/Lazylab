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

XML_EXPECTED = {
'juniper_vmxvcp_18':
"""<domain type='kvm'>
  <name>Test_Lab_Tested_VM_2</name>
  <description>#Auto-generated vm with lazylab
lab_name: Test_Lab
vm:
  name: Tested_VM_2
  os: juniper_vmxvcp
  version: 18</description>
  <memory unit='KiB'>1048576</memory>
  <currentMemory unit='KiB'>1048576</currentMemory>
  <vcpu placement='static'>1</vcpu>
  <os>
    <type arch='x86_64' machine='pc-0.13'>hvm</type>
  </os>
  <features>
    <acpi/>
    <apic/>
    <vmport state='off'/>
  </features>
  <cpu mode='host-model'>
    <model fallback='allow'/>
  </cpu>
  <clock offset='utc'>
    <timer name='rtc' tickpolicy='catchup'/>
    <timer name='pit' tickpolicy='delay'/>
    <timer name='hpet' present='no'/>
  </clock>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>destroy</on_crash>
  <pm>
    <suspend-to-mem enabled='no'/>
    <suspend-to-disk enabled='no'/>
  </pm>
  <devices>
    <emulator>/usr/bin/qemu-kvm</emulator>
    
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='/var/lib/libvirt/images/Test_Lab_Tested_VM_2_juniper_vmxvcp_18_A_template.qcow2'/>
      <target dev='sda' bus='virtio'/>
      <boot order='1'/>
    </disk>
    
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='/var/lib/libvirt/images/Test_Lab_Tested_VM_2_juniper_vmxvcp_18_B_template.qcow2'/>
      <target dev='sdb' bus='virtio'/>
      <boot order='2'/>
    </disk>
    
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='/var/lib/libvirt/images/Test_Lab_Tested_VM_2_juniper_vmxvcp_18_C_template.qcow2'/>
      <target dev='sdc' bus='virtio'/>
      <boot order='3'/>
    </disk>
    
    <controller type="pci" index="0" model="pci-root"/>
    <controller type="virtio-serial" index="0">
    </controller>
    <controller type="sata" index="0">
    </controller>
    <controller type="usb" index="0" model="piix3-uhci">
    </controller>
    
    <interface type='network'>
      <source network='default'/>
      <model type='e1000'/>
      
      <link state='down'/>
      
      <address type='pci' domain='0x0000' bus='0x00' function='0x0'/>
    </interface>
    
    <interface type='network'>
      <source network='default'/>
      <model type='e1000'/>
      
      <link state='down'/>
      
      <address type='pci' domain='0x0000' bus='0x00' function='0x0'/>
    </interface>
    
    <interface type='network'>
      <source network='Unknown_net'/>
      <model type='e1000'/>
      
      <address type='pci' domain='0x0000' bus='0x00' function='0x0'/>
    </interface>
    
    <serial type='tcp'>
      <source mode='bind' host='127.0.0.1' service='5002'/>
      <protocol type='telnet'/>
      <target type='isa-serial' port='1'>
        <model name='isa-serial'/>
      </target>
    </serial>
    <console type='tcp'>
      <source mode='bind' host='127.0.0.1' service='5002'/>
      <protocol type='telnet'/>
      <target type='serial' port='1'/>
    </console>
    <input type='mouse' bus='ps2'/>
    <input type='keyboard' bus='ps2'/>
    <graphics type='spice' autoport='yes'>
      <listen type='address'/>
      <image compression='off'/>
    </graphics>
    <video>
      <model type='qxl' ram='65536' vram='65536' vgamem='16384' heads='1' primary='yes'/>
    </video>
    <memballoon model='virtio'>
    </memballoon>
  </devices>
</domain>""",
'juniper_vmx_14':
"""<domain type='kvm'>
  <name>Test_Lab_Tested_VM_1</name>
  <description>#Auto-generated vm with lazylab
lab_name: Test_Lab
vm:
  name: Tested_VM_1
  os: juniper_vmx
  version: 14</description>
  <memory unit='KiB'>1048576</memory>
  <currentMemory unit='KiB'>1048576</currentMemory>
  <vcpu placement='static'>1</vcpu>
  <os>
    <type arch='x86_64' machine='pc-i440fx-3.0'>hvm</type>
    <boot dev='hd'/>
  </os>
  <features>
    <acpi/>
    <apic/>
    <vmport state='off'/>
  </features>
  <cpu mode='custom' match='exact' check='partial'>
    <model fallback='allow'>Nehalem</model>
  </cpu>
  <clock offset='utc'>
    <timer name='rtc' tickpolicy='catchup'/>
    <timer name='pit' tickpolicy='delay'/>
    <timer name='hpet' present='no'/>
  </clock>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>destroy</on_crash>
  <pm>
    <suspend-to-mem enabled='no'/>
    <suspend-to-disk enabled='no'/>
  </pm>
  <devices>
    <emulator>/usr/bin/qemu-kvm</emulator>
    
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='/var/lib/libvirt/images/Test_Lab_Tested_VM_1_juniper_vmx_14_template.qcow2'/>
      <target dev='hda' bus='ide'/>
      <address type='drive' controller='0' bus='0' target='0' unit='0'/>
    </disk>
    
    <controller type='usb' index='0' model='ich9-ehci1'>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x08' function='0x7'/>
    </controller>
    <controller type='pci' index='0' model='pci-root'/>
    <controller type='ide' index='0'>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x1'/>
    </controller>
    <controller type='virtio-serial' index='0'>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x07' function='0x0'/>
    </controller>
    
    <interface type='network'>
      <source network='default'/>
      <model type='virtio'/>
      
      <link state='down'/>
      
      <address type='pci' domain='0x0000' bus='0x00' function='0x0'/>
    </interface>
    
    <interface type='network'>
      <source network='default'/>
      <model type='virtio'/>
      
      <link state='down'/>
      
      <address type='pci' domain='0x0000' bus='0x00' function='0x0'/>
    </interface>
    
    <interface type='network'>
      <source network='Unknown_net'/>
      <model type='virtio'/>
      
      <address type='pci' domain='0x0000' bus='0x00' function='0x0'/>
    </interface>
    
    <serial type='tcp'>
      <source mode='bind' host='127.0.0.1' service='5001'/>
      <protocol type='telnet'/>
      <target type='isa-serial' port='1'>
        <model name='isa-serial'/>
      </target>
    </serial>
    <console type='tcp'>
      <source mode='bind' host='127.0.0.1' service='5001'/>
      <protocol type='telnet'/>
      <target type='serial' port='1'/>
    </console>
    <input type='mouse' bus='ps2'/>
    <input type='keyboard' bus='ps2'/>
    <graphics type='spice' autoport='yes'>
      <listen type='address'/>
      <image compression='off'/>
    </graphics>
    <video>
      <model type='qxl' ram='65536' vram='65536' vgamem='16384' heads='1' primary='yes'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
    </video>
    <memballoon model='virtio'>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x0a' function='0x0'/>
    </memballoon>
  </devices>
</domain>"""
}

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
        """Testing clone volume and delete volume for every device in list"""
        for distribution, device in self.devices.items():
            
            # Cloning volumes
            with self.subTest(action='clone', distribution=distribution):
                device.clone_volume()
                
                template_volume_list = TEMPLATE_IMAGE_LIST.get(device.distribution)
                for template_volume_name in template_volume_list:
                    with libvirt.open('qemu:///system') as conn: 
                        volume_pool = conn.storagePoolLookupByName(VOLUME_POOL_NAME)
                        volume_pool_xml_root = ElementTree.fromstring(volume_pool.XMLDesc())
                        target = next(volume_pool_xml_root.iter('target'))
                        volume_pool_path = next(target.iter('path')).text
                        clone_to_path = f'{volume_pool_path}/{device.vm_name}_{template_volume_name}'
                self.assertTrue(os.path.exists(clone_to_path))
                
            with self.subTest(action='delete', distribution=distribution):
                device.delete_volume()
                self.assertTrue(not (os.path.exists(clone_to_path)))
    
    
    def test_create_destroy_get_tcp_port_get_vm_networks(self):
        for distribution, device in self.devices.items():
            
            # Testing create
            with self.subTest(action='create', distribution=distribution):
                device.create_net()
                device.create_vm()
                with libvirt.open('qemu:///system') as conn:
                    dom = conn.lookupByName(device.vm_name) 
                    flag = bool(dom.isActive())
                self.assertTrue(flag)
            
            # Testing get_vm_networks
            with self.subTest(action='get_vm_networks', distribution=distribution):
                interfaces_we_get = device.vm_parameters['interfaces']
                interfaces_we_want_to_get = TEST_VM_PARAMETERS[distribution].get('interfaces')
                self.assertEqual(interfaces_we_get, interfaces_we_want_to_get)
                
            # Testing get_vm_tcp_port
            with self.subTest(action='get_vm_tcp_port', distribution=distribution):
                expected_vm_tcp_port = device.port
                device.get_vm_tcp_port()
                gotten_vm_tcp_port = device.port
                self.assertEqual(expected_vm_tcp_port, gotten_vm_tcp_port)
            
            # Testing destroy_vm
            with self.subTest(action='delete', distribution=distribution):
                flag = False
                device.destroy_vm()
                
                with libvirt.open('qemu:///system') as conn:
                    try:
                        dom = conn.lookupByName(device.vm_name)
                    except libvirt.libvirtError as err:
                        
                        # checking if libvirt error code is
                        # 42 - VIR_ERR_NO_DOMAIN. If not - exit the script
                        flag = bool(err.get_error_code() == 42)
                
                self.assertTrue(flag)
                
            
            # Testing destroy second time
            with self.subTest(action='second_delete', distribution=distribution):
                self.assertTrue(device.destroy_vm() == 0)
            
            # Testing destroy net
            with self.subTest(action='destroy net', distribution=distribution):
                with libvirt.open('qemu:///system') as conn:
                    network = conn.networkLookupByName('Unknown_net')
                    network.destroy()
                    try:
                        network = conn.networkLookupByName('Unknown_net')
                    except libvirt.libvirtError as err:
                        
                        # checking if libvirt error code is
                        # 43 - VIR_ERR_NO_NETWORK. If not - exit the script
                        flag = bool(err.get_error_code() == 43)
                self.assertTrue(flag)
        return 0
        
    def test_a_create_xml(self):
        for distribution, device in self.devices.items():
            # Testing clone
            with self.subTest(action='create_xml', distribution=distribution):
                device.create_xml()
                print(device.vm_xml_config)
                print(XML_EXPECTED.get(distribution))
                self.assertTrue(device.vm_xml_config == XML_EXPECTED.get(distribution))
                
        return 0
