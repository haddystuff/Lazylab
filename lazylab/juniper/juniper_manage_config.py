"""Base Juniper manageconfig class"""
from abc import ABC
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos import exception
from lazylab.base.base_manage_config import BaseManageConfig 
from lazylab.base.base_decorators import BaseDecorators
from lazylab.config_parser import PASSWORD_LIST
import telnetlib
import logging


logger = logging.getLogger("lazylab.juniper.juniper_manage_config")

class JuniperManageConfig(BaseManageConfig, ABC):
    """
    This is base juniper manageconfig class, you have to inherit from it when 
    writing new os manage_config class.
    """
    
    def waiting(self):
        """This method waiting until it find "login " in console output"""

        # Openning telnet connection
        with telnetlib.Telnet('127.0.0.1', self.port, 5) as tn:
            
            # just to be sure sending \n\r
            tn.write(b'\n\r')
            
            # read until we catch login prompt 
            output = tn.read_until(b'login: ', 400).decode('utf-8')
            
            logger.info(f'got this output while waiting:\n\n{output}')

        return 0
    
    @BaseDecorators.preconfigure
    def configure_vm(self):
        """Configuring method"""
        
        #connecting to device, loading config and commiting
        try:
            with Device(host='127.0.0.1', user='root', mode='telnet', 
                        port=str(self.port), console_has_banner=True) as dev:
                with Config(dev, mode='exclusive') as config:
                    
                    # loading and commiting config
                    config.load(self.vm_config, format="text", overwrite=True)
                    config.commit()
        
        except exception.ConfigLoadError as err:
            
            logger.warning(f'bad config for {self.vm_name}')
            
        except Exception as err:
            
            logger.warning('{err}')
            
        return 0
    

    def get_vm_config(self):
        """
        This method gets self.vm_config(configuration string)
        It work realy bad if first password isn't right one, so you can make
        only one try by now. We neet to fix this in future
        """
        
        # get console port
        self.get_vm_tcp_port()
        
        # iterating through password list
        for key, password in PASSWORD_LIST:
            try:
                with Device(host='127.0.0.1', user='root', password=password, 
                            mode='TELNET', port=str(self.port),
                            console_has_banner=True) as dev:
                                
                    # Getting config
                    candidate_config = dev.cli('show configuration', 
                                               format='text', 
                                               warning=False)
                    # Second way to get config
                    #candidate_config = dev.rpc.get_config(normalize=False, 
                    #                                      options={'inherit':'inherit',
                    #                                               'database':'committed',
                    #                                               'format':'text'}).text

                    # saving config
                    self.vm_config = self.config_purifier(candidate_config)
                
                #if password is correct break from loop    
                break
                
            except exception.ConnectAuthError as err:
                
                logger.error('{err}')
                print('wrong password, please change it in lazylab.conf')
                
                exit(1)
                
        return 0
        
    def config_purifier(self, candidate_config):
        """
        This method purify config from unnecessary string:
        "## Last commit: 2020-01-17 09:58:44 UTC by root"
        This method is Juniper specific.
        :config(str) - config string to purify
        """
        
        # Creating empty config list
        config = []
        
        # Filter lines in candidate list
        for line in candidate_config.splitlines():
            if '## Last commit:' not in line:
                config.append(line)
        config = '\n'.join(config)
        
        return config
