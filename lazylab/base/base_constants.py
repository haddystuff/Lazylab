"""Constants for base module"""


DEFAULT_VM_PARAMETERS = {'name': 'Unknown_VM', 
                         'os': 'Unknown_OS',
                         'version': 0, 
                         'interfaces': {'ge-0/0/0': 'Unknown_net'}}

# waiting timer for dump timer in BaseManageConfig
WAITING_TIMER = 2000

# managment net name
MANAGMENT_NET_NAME = 'default'
