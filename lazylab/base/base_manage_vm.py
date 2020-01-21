"""Base vm manager"""
from lazylab.config_parser import *
from lazylab.constants import TEMPLATE_IMAGE_LIST, INTERFACE_PREFIX
from lazylab.constants import VOLUME_CONFIG_TEMPLATE_NAME, MANAGMENT_NET_NAME
from lazylab.constants import INTERFACE_OFFSET, DEVICE_DESCRIPTION_MAIN_STR
from lazylab.constants import TEMPLATE_VOLUME_POOL_NAME
from lazylab.constants import TEMPLATE_DIRECTORY_PATH, NET_CONFIG_TEMPLATE_NAME
from lazylab.base.base_constants import DEFAULT_VM_PARAMETERS
import libvirt
import os
import logging
from xml.etree import ElementTree
from jinja2 import Environment, FileSystemLoader
from abc import ABC


logger = logging.getLogger(__name__)

# Create enviroment for jinja2
env = Environment(loader=FileSystemLoader(TEMPLATE_DIRECTORY_PATH))

class BaseManageVM(ABC):
    """Base vm manager"""
    def __init__(self, *args, **kvargs):
        """
        This is the base class you have to inherit from when writing new manage
        classes.
        :param lab_name(str): name of lab.
        :param vm_parameters(dict): dictionary with vm parameters. Neet to read
        with one from config.yml - file with all of vm parameters and topology.
        Usually looks like this: {'name': 'router2', 
                                  'os': 'cisco_iosxr',
                                  'version': 15,
                                  'interfaces': {'ge-0/0/0': 'Vlan1', 
                                                 'ge-0/0/1': 'Vlan2'}
                                  }
        :param port(int): telnet port number, with use to get conlsole to vm.
        :param virt_conn: libvirt connection object.
        :param config_file_object(file): file object of vm config file. If
        there's no config file then value of config_file_object must me "None".
        :return:
        """
        
        # Unpacking kvargs
        self.lab_name = kvargs.get('lab_name', 'Unknown_lab')
        self.vm_parameters = kvargs.get('vm_parameters', DEFAULT_VM_PARAMETERS)
        self.vm_short_name = self.vm_parameters.get('name')
        self.port = kvargs.get('port', None)
        self.vm_config = kvargs.get('vm_config', None)
        
        # Setting more variables and unpacking self.vm_parameters
        self.vm_name = self.lab_name + '_' + self.vm_short_name
        self.os = self.vm_parameters.get('os')
        self.version = str(self.vm_parameters.get('version'))
        self.distribution = self.os + '_' + self.version
        
        # Getting some variables from constants
        self.interface_offset = INTERFACE_OFFSET[self.distribution]
        self.template_volume_list = TEMPLATE_IMAGE_LIST.get(self.distribution)
        self.interface_prefix = INTERFACE_PREFIX.get(self.distribution)
        
        # Setting description for vm
        self.vm_discription = f"{DEVICE_DESCRIPTION_MAIN_STR}\n"\
                              f"lab_name: {self.lab_name}\n"\
                              f"vm:\n"\
                              f"  name: {self.vm_parameters.get('name')}\n"\
                              f"  os: {self.vm_parameters.get('os')}\n"\
                              f"  version: {self.version}"
                              
        logger.info(f'initialising new vm object:{self.vm_parameters}')

    def clone_volume(self):
        """
        This method creates vm volume by cloning template volume.
        To create new volume we need jinja2 template  wich is in "xml_configs"
        directory
        """
        
        with libvirt.open('qemu:///system') as self.virt_conn:
            
            for template_volume_name in self.template_volume_list:
                
                # Naming volume
                volume_name = f'{self.vm_name}_{template_volume_name}'
                
                # Getting jinja2 template file
                template = env.get_template(VOLUME_CONFIG_TEMPLATE_NAME)
                
                # Rendering jinja2 template
                volume_xml_config = template.render(volume_name=volume_name)
                
                # Connecting to storage pools
                volume_pool = self.virt_conn.storagePoolLookupByName(VOLUME_POOL_NAME)
                template_volume_pool = self.virt_conn.storagePoolLookupByName(TEMPLATE_VOLUME_POOL_NAME)
                
                # Logging
                logger.info(f'Creating new volume {volume_name}')
                
                # Cloning volume from existing one
                stgvol = template_volume_pool.storageVolLookupByName(template_volume_name)
                stgvol2 = volume_pool.createXMLFrom(volume_xml_config, stgvol, 0)
                
        return 0


    def create_xml(self):
        """This method create vm xml for libvirt from jinja2 template."""
        
        with libvirt.open('qemu:///system') as self.virt_conn:
            
            # Creating nets list wich will contain all virtuall networks names
            nets = []
            
            # Usually several first interfaces in virtual network devices are
            # managment or internal use interfaces so we need add first
            # n = self.interface_offset interfaces to managment net
            for n in range(self.interface_offset):
                nets.append(MANAGMENT_NET_NAME)
            
            # append usuall interfaces according to vm_parameters 
            for interface, lan in self.vm_parameters['interfaces'].items():
                nets.append(lan)
            
            # Creating volume_location_list wich will contain all volume 
            # locations
            volume_location_list = []
            
            # Adding volume locations to volume_location_list
            for template_volume_name in self.template_volume_list:
                
                volume_location = f'{VOLUME_POOL_DIRECTORY}{self.vm_name}_{template_volume_name}'
                volume_location_list.append(volume_location)
            
            # Logging
            logger.info(f'Create volume location list:{volume_location_list}')
            
            # Opening vm xml jinja2 template
            vm_xml_name = f'{self.distribution}_jinja_template.xml'
            template = env.get_template(vm_xml_name)
            
            # Rendering template so we get config for our vm
            config_string = template.render(vm_name=self.vm_name, 
                                            description=self.vm_discription, 
                                            port_number=str(self.port), 
                                            nets=nets, 
                                            volume_location_list=volume_location_list,
                                            managment_net_name=MANAGMENT_NET_NAME)
                                            
            # setting vm_xml_config parametr
            self.vm_xml_config = config_string
            
        return 0


    def create_vm(self):
        """This method defines and creates vm from xml config."""
        
        # Cloning volume
        self.clone_volume()
        
        #Creating xml
        self.create_xml()
        
        # Defining vm
        with libvirt.open('qemu:///system') as self.virt_conn:
            
            print('Creating vm', self.vm_name)
            
            # Logging
            logger.info(f'Creating vm with xml:/n{self.vm_xml_config}')
            
            # Setting xml for new libvirt domain 
            dom = self.virt_conn.defineXML(self.vm_xml_config)
            
            # Logging
            logger.info(f'Creating {self.vm_name}')
            
            # Creating and starting vm
            dom.create()
            
            # Logging
            logger.info(f'{self.vm_name} started')
            
        return 0


    def destroy_vm(self):
        """This method destroys(deletes) existing vm."""
        
        with libvirt.open('qemu:///system') as self.virt_conn:
            
            print(f'Deleting {self.vm_name}')
            logger.info(f'Deleting {self.vm_name}')
            
            try:
                
                # Getting domain(vm) object
                dom = self.virt_conn.lookupByName(self.vm_name)
                
            except libvirt.libvirtError as err:
                
                # checking if libvirt error code is
                # 42 - VIR_ERR_NO_DOMAIN. If not - exit the script
                if err.get_error_code() != 42:
                    logger.error(f'{err.get_error_message()}')
                    exit(1)
                
                logger.info(f'{err.get_error_message()}')

            else:
                
                # Stoping domain if domain exist
                try:
                    dom.destroy()
                    
                except libvirt.libvirtError as err:
                    
                    # checking if libvirt error code is
                    # 55 - VIR_ERR_OPERATION_INVALID. If not - exit the script
                    if err.get_error_code() != 55:
                        logger.error(f'{err.get_error_message()}')
                        exit(1)
                    
                    logger.info(f'{err.get_error_message()}')
                    print('Domain', self.vm_name, 'is already stoped')
                
                # Undefine domain
                dom.undefine()
                
        # Deleting volume
        self.delete_volume()
        
        return 0


    def delete_volume(self):
        """
        This method deletes volume of vm.
        """
        
        with libvirt.open('qemu:///system') as self.virt_conn:
            
            # Connect to pool
            pool = self.virt_conn.storagePoolLookupByName(VOLUME_POOL_NAME)
            
            for template_volume_name in self.template_volume_list:
                
                #Getting volume name
                volume_name = f'{self.vm_name}_{template_volume_name}'
                
                try:
                    
                    # Getting volume object
                    stgvol = pool.storageVolLookupByName(volume_name)
                    
                except libvirt.libvirtError as err:
                    
                    # checking if libvirt error code is
                    # 50 - VIR_ERR_NO_STORAGE_VOL
                    if err.get_error_code() != 50:
                        logger.error(f'{err.get_error_message()}')
                        exit(1)
                    
                    logger.warning(f'Volume {volume_name} is already deleted')
                
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
            
            # Getting domain(vm) object
            dom = self.virt_conn.lookupByName(self.vm_name)
            
            # Getting root of domain(vm) xml object
            dom_xml_root = ElementTree.fromstring(dom.XMLDesc(0))
            
            # iterating through xml until find 'console' element 
            console = next(dom_xml_root.iter('console'))
            
            # get 'service' value
            tcp_port = console[0].get('service')
            
        self.port = tcp_port
        
        return 0


    def create_net(self):
        """
        This method creates virtual network for vm.
        """
        with libvirt.open('qemu:///system') as self.virt_conn:
            
            # iterating through net list
            for interface, net in self.vm_parameters.get('interfaces').items():
                
                #Opening and rendering jinja virtual network template
                template = env.get_template(NET_CONFIG_TEMPLATE_NAME)
                config_string = template.render(net_name = net)
                
                #Creating net
                try:
                    
                    network = self.virt_conn.networkCreateXML(config_string)
                    
                except libvirt.libvirtError as err:
                    
                    # checking if libvirt error code is
                    # 9 - VIR_ERR_OPERATION_FAILED
                    if err.get_error_code() != 9:
                        logger.error(f'{err.get_error_message()}')
                        exit(1)
                    
                    else:
                        
                        logger.info(f'{err.get_error_message()}')
                    
                logger.info(f'Created net {net}')
                
        return 0
        
    def get_vm_networks(self):
        
        with libvirt.open('qemu:///system') as self.virt_conn:
            
            # Getting domain(vm) object
            dom = self.virt_conn.lookupByName(self.vm_name)
            
            # Getting root of domain xml
            dom_xml_root = ElementTree.fromstring(dom.XMLDesc(0))  
            
            # Creating interface_dictionary
            interface_dictionary = {}
            
            # iterating through interfaces in dom_xml_root also getting indexes
            for interface_number,interface_xml in enumerate(dom_xml_root.iter('interface')): 
                
                # continue if its managment interface
                if interface_number - self.interface_offset < 0:
                    continue
                
                # getting the network part of interface_xml
                network = next(interface_xml.iter('source')) 
                
                # setting key string for vm_parameters['interfaces'] dictionary
                interface_key = self.interface_prefix + str(interface_number)
                
                # getting connected to interface network name
                # In KVM thouse networks are bridges
                network_name = network.get('network', 'unknown_network')
                
                # Adding to interface_dictionary new key + value
                interface_dictionary[interface_key] = network_name
        
        # adding to vm_parameters interface dictionary         
        self.vm_parameters['interfaces'] = interface_dictionary
        
        return 0
