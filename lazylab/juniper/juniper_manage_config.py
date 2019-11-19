from abc import ABC
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos import exception
from lazylab.base.base_manage_config import BaseManageConfig 
from lazylab.config_parser import PASSWORD_LIST
from time import sleep

class JuniperManageConfig(BaseManageConfig, ABC):
    """
    This is base juniper manageconfig class, you have to inherit from it when 
    writing new os manage_config class.
    """
    
    
    #Configuring method
    def configure_vm(self):
        
        #Checking if config is existing
        if self.vm_config == None:
            print("No config file. Using default settings")
            return 0
        
        #connecting to device, loading config and commiting
        try:
            with Device(host='127.0.0.1', user='root', mode='telnet', port=str(self.port)) as dev:
                with Config(dev, mode='exclusive') as cu:
                    try:
                        cu.load(self.vm_config, format="text", overwrite=True)
                        cu.commit()
                    except Exception as err:
                        print(err)
                        print('Bad config file\n Using default config')
        except Exception as err:
            print (err)
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
                with Device(host='127.0.0.1', user='root', password=password, mode='TELNET', port=str(self.port)) as dev:
                    self.vm_config = (dev.cli("show configuration", format='text', warning=False))
                break
            except exception.ConnectAuthError as err:
                print(err)
                continue
                exit(1)
        return 0
