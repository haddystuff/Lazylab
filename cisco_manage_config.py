from abc import ABC
import telnetlib
from base_manage_config import BaseManageConfig

class CiscoManageConfig(BaseManageConfig, ABC):
    """
    This is base Cisco manageconfig class, you have to inherit from it when writing new os manage_config class.
    """

    def configure_vm(self):
        #Need to create new method to check if file exist
        if self.vm_config == None:
            print("No config file. Using default settings")
            return(0)
        try:
            tn = telnetlib.Telnet("127.0.0.1", str(self.port), 5)
            tn.write(b"\n\r") 
            print(tn.read_until(b"name: ", 5)) 
            tn.write(b"root\r") 
            print(tn.read_until(b"word: ", 5)) 
            tn.write(b"root\r") 
            print(tn.read_until(b"#", 5)) 
            tn.write(b"configure\n") 
            print(tn.read_until(b"#", 5))
            tn.write(self.vm_config.encode('utf-8'))
            print(tn.read_until(b"[cancel]:", 5))
            tn.write(b"yes\n") 
            tn.write(b"exit\n") 
            tn.write(b"exit\n") 
        except Exception as err:
            print (err)
        return(0)
        
