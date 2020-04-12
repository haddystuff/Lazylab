"""YAML_Parser Module"""
import yaml
from lazylab.constants import POSSIBLE_OS_LIST


def parse_yaml(conf_yaml):
    """
    This function check if yaml file has right structure and syntax.
    I need to modify this code in future so we can check all syntax in yaml file.
    """
    
    # Loading yaml to dict
    conf_dict = yaml.load(conf_yaml, Loader=yaml.FullLoader)
    
    # Getting list of vms.
    vms_parameters_list = conf_dict.get('vms')
    
    # Check if vms is actualy existing
    if vms_parameters_list is None:
        print('No \"vms\" block in config file')
        exit(1)
    
    # Check if lab name existing
    if conf_dict.get('lab_name') is None:
        print('No \"lab_name\" block in config file')
        exit(1)
    
    # Check vm one by one.
    for vm_parameters in vms_parameters_list:
        
        # Check if name of vm is actially exist
        if vm_parameters.get('name') is None:
            print('No \"VM Name\" block in config file')
            exit(1)
        
        # Check if vm has right os and version(distibution in this context)
        distribution = vm_parameters.get('os') + '_' + str(vm_parameters.get('version'))
        
        if not(distribution in POSSIBLE_OS_LIST):
            print('Yaml file has bad syntax: wrong os name')
            exit(1)
        
    return conf_dict
