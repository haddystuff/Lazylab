INTERFACE_OFFSET = {'cisco_iosxr_15': 1,
                    'juniper_vmx_14': 2,
                    'juniper_vmxvcp_18': 2}

INTERFACE_PREFIX = {'cisco_iosxr_15': 'ge',
                    'juniper_vmx_14': 'em',
                    'juniper_vmxvcp_18': 'ge'}

DISTRIBUTION_IMAGE = {'juniper_vmx_14': ['juniper_vmx_14_template.qcow2'],
                      'juniper_vmxvcp_18': ['juniper_vmxvcp_18_A_template.qcow2', 
                                            'juniper_vmxvcp_18_B_template.qcow2', 
                                            'juniper_vmxvcp_18_C_template.qcow2'],
                      'cisco_iosxr_15': ['cisco_iosxr_15_template.qcow2']}

DEFAULT_VM_PARAMETERS = {'name': 'Unknown_VM', 
                         'os': 'Unknown_OS',
                         'version': 0, 
                         'interfaces': {'ge-0/0/0': 'Unknown_net'}}
