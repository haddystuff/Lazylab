Tasker Structure
======================

Tasker is core module.
It consists of Class named Tasker that implements business rules.

Usually GUI module(it only has "cli GUI" by now) creates object of Tasker class and 
runs simple named methods.
It looks like this:

``task = Tasker()
task.deploy_lab(lab_name)``

Logic of Tasker class object is quite simple:
First it usually creates dictionary of VMs objects.
VM object(called "devices" in code) - object that describe vm.
Purpose of this object is to fully control one vm.
Usually type of this object is self explanatory, for example: ``JuniperVmx14ManageAll``.
All of this objects usually creates by "Device Creator" submodule which runs by Tasker, for example:

``creator = DeviceCreator(**self.vms_attributes)``

``device = creator.create_device(lab_name=lab_name, vm_parameters=vm_parameters)``

device_creator is just small factory which generates devices(VMs) objects.
After dictionary of devices objects created Tasker runs some methods of this objects.
For example for lab deleting Tasker runs ``device.destroy_vm()``

===============================

Also there are more submodules in Tasker module:

1. tasker_helpers submodule is just a bunch of functions which helps Tasker to do his work.

2. downloader submodule helps tasker to download labs archives and template images.


================================

You can see full structure of lazylab in dependency graph.
