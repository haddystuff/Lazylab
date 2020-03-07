Base classes
=======================

Base classes are inherited by Manage Classes.

Manage Class - class which instances are VM objects.
VM object(called "devices" in code) - object that describe vm.
Purpose of this object is to fully control one vm.
Usually type of this object is self explanatory, for example: ``JuniperVmx14ManageAll``.

List of base classes:

1. BaseManageVM - generic class contains vm management methods that should be common for all VM object.

2. BaseManageConfig - special class that inherited by vendor specific ManageConfig classes. It contains abstract methods and some default methods for vendor specific ManageConfig classes to be inherit.

2. BaseQCOWSupport - class that contains qcow2 image format support

3. BasePersistencySupport - class that contains persistent libvirt domains(VMs) support

