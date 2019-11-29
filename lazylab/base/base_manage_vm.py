from lazylab.config_parser import *
import libvirt
import os
from xml.etree import ElementTree
from jinja2 import Template
import logging
from abc import ABC


logger = logging.getLogger('lazylab.base.base_manage_vm')

class BaseManageVM(ABC):
    def __init__(self, **kvargs):
        """
        This is the base class you have to inherit from when writing new manage
        objects.
        :param lab_name(str): name of lab.
        :param vm_parameters(dict): dictionary with vm parameters. Neet to read
        with one from config.yml - file with all of vm parameters and topology.
        Usually looks like this: {'name': 'router2', 
                                  'os': 'cisco_iosxr',
                                  'version': 15,
                                  'interfaces': {'ge-0/0/0': 'Vxlan1', 
                                                 'ge-0/0/1': 'Vxlan2'}
                                  }
        :param port(int): telnet port number, with use to get conlsole to vm.
        :param virt_conn: libvirt connection object.
        :param config_file_object(file): file object of vm config file. If
        there's no config file then value of config_file_object must me "None".
        :return:
        """
        self.lab_name = kvargs.get('lab_name', 'Unknown_lab')
        self.vm_parameters = kvargs.get('vm_parameters', DEFAULT_VM_PARAMETERS)
        self.vm_short_name = self.vm_parameters.get('name')
        self.port = kvargs.get('port', None)
        self.vm_config = kvargs.get('vm_config', None)
        self.vm_name = self.lab_name + '_' + self.vm_short_name
        self.os = self.vm_parameters.get('os')
        self.version = str(self.vm_parameters.get('version'))
        self.distribution = self.os + '_' + self.version
        self.vm_discription = f"#Auto-generated vm with lazylab\n"\
                              f"lab_name: {self.lab_name}\n"\
                              f"vm:\n"\
                              f"  name: {self.vm_parameters.get('name')}\n"\
                              f"  os: {self.vm_parameters.get('os')}\n"\
                              f"  version: {self.version}"
        self.wait_miliseconds = 2000
        self.interface_offset = INTERFACE_OFFSET[self.distribution]
        self.volume_list = DISTRIBUTION_IMAGE.get(self.distribution)
        logging.info(f'initialise new vm object{self.vm_parameters}')

    def clone_volume(self):
        """
        This method creates vm volume by cloning template volume.
        To create new volume we need jinja2 template  wich is in "xml_configs"
        directory
        """
        
        
        with libvirt.open('qemu:///system') as self.virt_conn:
            #Opening and rendering jinja template
            for template_volume_name in self.volume_list:
                with open(VOLUME_CONFIG_JINJA_TEMPLATE) as xml_jinja_template:
                    template = Template(xml_jinja_template.read())
                volume_name = self.vm_name + template_volume_name
                volume_xml_config = template.render(volume_name = volume_name)
                
                # Connecting to storage pools
                volume_pool = self.virt_conn.storagePoolLookupByName(VOLUME_POOL_NAME)
                template_volume_pool = self.virt_conn.storagePoolLookupByName(TEMPLATE_VOLUME_POOL_NAME)
                
                # Logging
                logging.info(f'Creating new volume {volume_name}')
                
                # Cloning volume from existing one
                stgvol = template_volume_pool.storageVolLookupByName(template_volume_name)
                stgvol2 = volume_pool.createXMLFrom(volume_xml_config, stgvol, 0)
        return 0


    def create_xml(self):
        """
        This method creating vm xml for libvirt from jinja2 template.
        """
        
        
        with libvirt.open('qemu:///system') as self.virt_conn:
            #Getting all virtuall networks names to nets[] list
            nets = []
            for n in range(self.interface_offset):
                nets.append(MANAGMENT_NET_NAME)
            #
            for interface, lan in self.vm_parameters['interfaces'].items():
                nets.append(lan)
            #
            volume_location_list = []
            for template_volume_name in self.volume_list:
                volume_location_list.append(VOLUME_POOL_DIRECTORY + 
                                            self.vm_name + 
                                            template_volume_name)
            
            #Logging
            logging.info(f'Create volume location list:{volume_location_list}')
            
            #Opening and rendering jinja template
            with open(PATH_TO_MODULE + "/xml_configs/" + self.distribution + '_jinja_template.xml') as xml_jinja_template:
                template = Template(xml_jinja_template.read())
            config_string = template.render(vm_name=self.vm_name, 
                                            description=self.vm_discription, 
                                            port_number=str(self.port), 
                                            nets=nets, 
                                            volume_location_list=volume_location_list,
                                            managment_net_name=MANAGMENT_NET_NAME)
            self.vm_xml_config = config_string
        return 0


    def create_vm(self):
        """
        This method defines and creates vm from existing xml config.
        """
        
        #Creating xml
        self.create_xml()
        
        # Defining vm
        with libvirt.open('qemu:///system') as self.virt_conn:
            print('Creating vm', self.vm_name)
            
            # Logging
            logging.info(f'Creating vm with xml:/n{self.vm_xml_config}')
            
            # Setting xml for new libvirt domain 
            dom = self.virt_conn.defineXML(self.vm_xml_config)
            
            # Creating and starting vm
            dom.create()
            
            # Logging
            logging.info(f'Starting {self.vm_name}')
            
        return 0


    def destroy_vm(self):
        """
        This method destroys(deletes) existing vm.
        """
        
        # Opening Libvirt connection
        with libvirt.open('qemu:///system') as self.virt_conn:
            print(f'Deleting {self.vm_name}')
            logging.info(f'Deleting {self.vm_name}')
            try:
                # Connect to domain
                dom = self.virt_conn.lookupByName(self.vm_name)
            except libvirt.libvirtError as err:
                
                # checking if libvirt error code is
                # 42 - VIR_ERR_OPERATION_INVALID
                if err.get_error_code() != 42:
                        logging.error(f'{err.get_error_message()}')
                        exit(1)
                logging.info(f'{err.get_error_message()}')

            else:
                # Stoping domain
                try:
                    
                    dom.destroy()
                    
                except libvirt.libvirtError as err:
                    
                    # checking if libvirt error code is
                    # 55 - VIR_ERR_OPERATION_INVALID
                    if err.get_error_code() != 55:
                        logging.error(f'{err.get_error_message()}')
                        exit(1)
                    
                    logging.info(f'{err.get_error_message()}')
                    print('Domain', self.vm_name, 'is already stoped')
                
                # Undefine domain
                dom.undefine()
        return 0


    def delete_volume(self):
        """
        This method deletes volume of existing vm.
        """
        with libvirt.open('qemu:///system') as self.virt_conn:
            # Connect to pool
            pool = self.virt_conn.storagePoolLookupByName(VOLUME_POOL_NAME)
            for template_volume_name in self.volume_list:
                volume_name = self.vm_name + template_volume_name
                try:
                    
                    # Getting volume object
                    stgvol = pool.storageVolLookupByName(volume_name)
                    
                except libvirt.libvirtError as err:
                    
                    # checking if libvirt error code is
                    # 50 - VIR_ERR_NO_STORAGE_VOL
                    if err.get_error_code() != 50:
                        logging.error(f'{err.get_error_message()}')
                        exit(1)
                    
                    logging.warning(f'Volume {volume_name} is already deleted')
                
                else:
                    # physically remove the storage volume from the underlying
                    # disk media
                    stgvol.wipe()
                    
                    # logically remove the storage volume from the storage pool
                    stgvol.delete()
        return 0


    def get_vm_tcp_port(self):
        """
        This method getting tcp port of console connection of existing vm.
        """
        with libvirt.open('qemu:///system') as self.virt_conn:
            #Getting tcp port from device xml file with ElementTree
            dom = self.virt_conn.lookupByName(self.vm_name)
            root = ElementTree.fromstring(dom.XMLDesc(0))
            console = next(root.iter('console'))
            tcp_port = console[0].get('service')
        self.port = tcp_port
        return 0


    def create_net(self):
        """
        This method creates virtual network for vm.
        """
        with libvirt.open('qemu:///system') as self.virt_conn:
            for interface, net in self.vm_parameters.get('interfaces').items():
                
                #Opening and rendering jinja virtual network template
                with open(NET_CONFIG_JINJA_TEMPLATE) as xml_jinja_template:
                    template = Template(xml_jinja_template.read())
                config_string = template.render(net_name = net)
                
                #Creating net
                try:
                    
                    network = self.virt_conn.networkCreateXML(config_string)
                    
                except libvirt.libvirtError as err:
                    
                    # checking if libvirt error code is
                    # 9 - VIR_ERR_OPERATION_FAILED
                    if err.get_error_code() != 9:
                        logging.error(f'{err.get_error_message()}')
                        exit(1)
                    
                    else:
                        
                        logging.info(f'{err.get_error_message()}')
                    
                    continue
                    
                logging.info(f'Create net {net}')
                
        return 0
        
    def get_vm_networks(self):
        with libvirt.open('qemu:///system') as self.virt_conn:
            vm_object = self.virt_conn.lookupByName(self.vm_name)
            vm_xml_root = ElementTree.fromstring(vm_object.XMLDesc(0))  
            interface_dictionary = {}
            self.interface_prefix = INTERFACE_PREFIX.get(self.distribution)
            for interface_number,interface in enumerate(vm_xml_root.iter('interface')): 
                if interface_number - self.interface_offset < 0:
                    continue
                network = next(interface.iter('source')) 
                interface_key = self.interface_prefix + str(interface_number)
                interface_dictionary[interface_key] = network.get('network')
        self.vm_parameters['interfaces'] = interface_dictionary
        return 0
