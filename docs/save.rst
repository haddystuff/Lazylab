Save
=================

``save`` command work logic can be seen below:

1. Parsing all VMs description which have {lab_name} in their names of special string('#Auto-generated vm with lazylab' by default)

2. Trying to connect and download config from VMs

3. Saving topology and parameter of that VMs to config.yml file.

4. Creating {new_lab_name}.lazy arhive which contains config.yml and raw VMs configs.
