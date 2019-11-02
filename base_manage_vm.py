from config_parser import *
import libvirt
import sys
import os
from xml.etree import ElementTree
from jinja2 import Template
import libvirt


class BaseManageVM(object):
    def __init__(self, lab_name, vm, port, vm_config):
        """
        This is the base class you have to inherit from when writing new manage objects.
        :param lab_name(str): name of lab.
        :param vm(dict): dictionary with vm parameters. Neet to read with one from config.yml - file with all of vm parameters and topology.
        :param port(int): telnet port number, with use to get conlsole to vm.
        :param virt_conn: libvirt connection object.
        :param config_file_object(file): file object of vm config file. If there's no config file then value of config_file_object must me "None".
        :return:
        """
        self.lab_name = lab_name
        self.vm = vm
        self.port = port
        self.vm_config = vm_config
        self.vm_name = self.lab_name + '_' + vm['name']
        self.vm_discription = "auto-generated vm with autodeploytool for " + self.lab_name + " lab"
        self.distribution = vm['os'] + '_' + str(vm['version'])
        self.wait_miliseconds = 2000


    def clone_volume(self):
        """
        This method creates vm volume by cloning template volume.
        To create new volume we need jinja2 template  wich is in "xml_configs" directory
        """
        with libvirt.open('qemu:///system') as self.virt_conn:
            #Opening and rendering jinja template
            with open(os.path.join(sys.path[0] + "/xml_configs/" + 'volume_config_jinja_template.xml')) as xml_jinja_template:
                template = Template(xml_jinja_template.read())
            self.volume_xml_config = template.render(vm_name = self.vm_name)
            
            # Connecting to storage pool
            pool = self.virt_conn.storagePoolLookupByName(VOLUME_POOL_NAME)
            
            # Cloning volume from existing one
            stgvol = pool.storageVolLookupByName(self.distribution + '_template.qcow2')
            print('Creating new volume')
            stgvol2 = pool.createXMLFrom(self.volume_xml_config, stgvol, 0)
        return(0)


    def create_xml(self):
        """
        This method creating vm xml for libvirt from jinja2 template.
        """
        with libvirt.open('qemu:///system') as self.virt_conn:
            #Getting all virtuall networks names to nets[] list
            nets = []
            for interface, lan in self.vm['interfaces'].items():
                nets.append(lan)
            
            #Opening and rendering jinja template
            with open(os.path.join(sys.path[0] + "/xml_configs", self.distribution + '_jinja_template.xml')) as xml_jinja_template:
                template = Template(xml_jinja_template.read())
            config_string = template.render(vm_name = self.vm_name, description = self.vm_discription, port_number = str(self.port), nets = nets, volume_location = (VOLUME_POOL_DIRECTORY + self.vm_name))
            self.vm_xml_config = config_string
        return(0)


    def create_vm(self):
        """
        This method defines and creates vm from existing xml config.
        """
        #Creating xml
        self.create_xml()
        # Defining vm
        with libvirt.open('qemu:///system') as self.virt_conn:
            print('Creating vm', self.vm_name)
            dom = self.virt_conn.defineXML(self.vm_xml_config)
            # Creating and starting vm
            dom.create()
            print('Starting', self.vm_name)
        return(0)


    def destroy_vm(self):
        """
        This method destroys(deletes) existing vm.
        """
        with libvirt.open('qemu:///system') as self.virt_conn:
            try:
                # Connect to domain
                dom = self.virt_conn.lookupByName(self.vm_name)
                # Stoping domain
                try:
                    dom.destroy()
                except Exception:
                    print('Domain', self.vm_name, 'is already stoped')
                # Undefine domain
                dom.undefine()
            except Exception:
                print('Domain', self.vm_name, 'is already deleted')
        return(0)


    def delete_volume(self):
        """
        This method deletes volume of existing vm.
        """
        with libvirt.open('qemu:///system') as self.virt_conn:
            # Connect to pool
            pool = self.virt_conn.storagePoolLookupByName(VOLUME_POOL_NAME)
            try:
                # Getting volume object
                stgvol = pool.storageVolLookupByName(self.vm_name)
                
                # physically remove the storage volume from the underlying disk media
                stgvol.wipe()
                
                # logically remove the storage volume from the storage pool
                stgvol.delete()
                
            except Exception:
                print('Volume', self.vm_name, 'is already deleted')
        return(0)


    def get_vm_tcp_port(self):
        """
        This method getting tcp port of console connection of existing vm.
        """
        with libvirt.open('qemu:///system') as self.virt_conn:
            dom = conn.lookupByName(self.vm_name)
            root = ElementTree.fromstring(dom.XMLDesc(0))
            console = next(root.iter('console'))
            tcp_port = console[0].get('service')
        self.port = tcp_port
        return(0)


    def create_net(self):
        """
        This method creates virtual network for vm.
        """
        with libvirt.open('qemu:///system') as self.virt_conn:
            for interface, net in self.vm['interfaces'].items():
                
                #Opening and rendering jinja template
                with open(os.path.join(sys.path[0] + "/xml_configs/" + 'net_config_jinja_template.xml')) as xml_jinja_template:
                    template = Template(xml_jinja_template.read())
                config_string = template.render(net_name = net)
                
                #Creating net
                try:
                    network = self.virt_conn.networkCreateXML(config_string)
                except Exception as err:
                    continue
                print(net)
        return(0)
