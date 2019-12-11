"""Base Juniper manageconfig class"""
from abc import ABC
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos import exception
from lazylab.base.base_manage_config import BaseManageConfig 
from lazylab.config_parser import PASSWORD_LIST
import telnetlib
import logging


logger = logging.getLogger('lazylab.juniper.juniper_manage_config')

class JuniperManageConfig(BaseManageConfig, ABC):
    """
    This is base juniper manageconfig class, you have to inherit from it when 
    writing new os manage_config class.
    """
    def waiting(self):
        """This method waiting until it find "login " in console output"""

        # Openning telnet connection
        with telnetlib.Telnet("127.0.0.1", self.port, 5) as tn:
            
            # just to be sure sending \n\r
            tn.write(b"\n\r")
            
            # read until we catch login prompt 
            output = tn.read_until(b"login: ", 400)
            
            logging.info(f'got this output while waiting:\n\n{output}')

        return 0
    
    
    #Configuring method
    def configure_vm(self):
        
        #Checking if config is existing
        if not self.vm_config:
            
            logging.warning(f'No config file for {self.vm_name}. Skipping configuration step')
            
            return 0
        
        #connecting to device, loading config and commiting
        try:
            with Device(host='127.0.0.1', user='root', mode='telnet', port=str(self.port), console_has_banner=True) as dev:
                with Config(dev, mode='exclusive') as cu:
                    
                    # loading and commiting config
                    cu.load(self.vm_config, format="text", overwrite=True)
                    cu.commit()
        
        except exception.ConfigLoadError as err:
            print (type(err))
            exit(1)
        return 0
    
    
    #Save config method is in work, so please don't use it for now.
    def get_config_vm(self):
        """
        This method gets self.vm_config(configuration string)
        It work realy bad if first password isnt right one, so we neet
        to fix this in future
        """
        
        
        self.get_vm_tcp_port()
        for key, password in PASSWORD_LIST:
            try:
                print (password)
                with Device(host='127.0.0.1', user='root', password=password, mode='TELNET', port=str(self.port), console_has_banner=True) as dev:
                    self.vm_config = (dev.cli("show configuration", format='text', warning=False))
                break
            except exception.ConnectAuthError as err:
                print(err)
                print('wrong password')
                exit(1)
        return 0
