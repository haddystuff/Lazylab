Delete
=================

``lazylab-delete`` command work logic can be seen below:

1. Parsing all VMs description which have {lab_name} in their names of special string('#Auto-generated vm with lazylab' by default)

2. Trying to stop VMs

3. Trying to delete VMs
