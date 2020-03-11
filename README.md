Lazylab
======
Lazylab is network lab auto-deployment tool.

It's just a python module that can download vm configs, topology, images and deploy fully operation lab in one command.
You just need to choose lab from the Labs list.

Lazylab using libvirt API to KVM hypervisor.
It can be easily implemented to already running libvirt setup.
Lazylab fully compatible with virt-manager, cockpit-machines.

Install
--------------

### Fedora/Ubuntu

install libvirt

add your user to libvirt group
```
sudo usermod -a -G libvirt $(whoami)
```
clone lazylab with
```
git clone https://github.com/haddystuff/lazylab
```

Running
------------

You can mostly do three things:

1. Deploy lab you want with ``deploy`` argument, for example:
``lazylab deploy test_all`` - wich will deploy lab named 'test_all'.

2. Delete lab you want with ``delete`` argument, for example:
``lazylab delete test_all`` - wich will delete lab named 'test_all'.

3. Save lab you want with ``save`` and ``as`` arguments, for example:
``lazylab save test_all as test_all_v2`` - wich will save lab named 'test_all' as 'test_all_v2'.


Supported network devices
---------
Juniper VMX: 14, 18(vcp only)
Cisco iosxrv: 5


Labs list
---------
* test

* default
