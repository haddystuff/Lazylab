Vendors modules structure
========================

There are modules that called "Cisco" "Juniper" etc. in lazylab.

They consist of spetial abstract classes(a.k.a vendor classes) that inherited by Manage Classes.
Manage Class - class which instances are VM objects.
VM object(called "devices" in code) - object that describe vm.
Purpose of this object is to fully control one vm.
All of this objects usually creates by Tasker module.

As you can see vendor classes are responsible for a part of VM object functionality.
Part that depends on Vendor of VM.


For now vendor classes should define this methods:

1. configure_vm - connects to VM and commits new config to it.

2. get_vm_config - connects ot VM, read and save config to self.vm_config valuable.

