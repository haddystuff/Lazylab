"""Base Cisco manageconfig class"""
from abc import ABC
import telnetlib
from lazylab.base.base_manage_config import BaseManageConfig
from abc import ABC
import logging


logger = logging.getLogger(__name__)

class CiscoManageConfig(BaseManageConfig, ABC):
    """
    This is base Cisco manageconfig class, you have to inherit from it when
    writing new os manage_config class.
    """

    def configure_vm(self):
        
        # check if config exist
        if not self.vm_config:
            
            logger.warning(f'No config file for {self.vm_name}. Skipping configuration step')
            
            return(0)
    
        #Connecting to console using telnet
        with telnetlib.Telnet("127.0.0.1", str(self.port), 5) as tn:
        
            #just in case
            tn.write(b"\n\r") 
            
            # read until we find "name: " and saving output
            output = tn.read_until(b"name: ", 5)
            
            # logging output
            logger.info(output.decode('utf-8'))
            
            # sending "root\r"
            tn.write(b"root\r") 
            
            # reading
            output = tn.read_until(b"word: ", 5)
            
            # logging output
            logger.info(output.decode('utf-8'))
            
            # sending
            tn.write(b"root\r") 
            
            # reading
            output = tn.read_until(b"#", 5)
            
            # logging output
            logger.info(output.decode('utf-8'))
            
            # sending
            tn.write(b"configure\n") 
            
            # reading
            output = tn.read_until(b"#", 5)
            
            # logging output
            logger.info(output.decode('utf-8'))
            
            # getting config string
            config = self.vm_config.encode('utf-8')
            
            #sending config encoded in utf-8
            tn.write(config)
            
            # reading
            output = tn.read_until(b"[cancel]:", 5)
            
            # logging output
            logger.info(output.decode('utf-8'))
            
            # sending comminting commands
            tn.write(b"yes\n") 
            tn.write(b"exit\n") 
            tn.write(b"exit\n") 
            
        return(0)
    
    def save_vm(self):
        
        print('no save avalible for cisco right now')
        
        return 0
