#!/bin/bash 
#this is initial script for lazylab. You need to run it as root before you can use lazylab


systemctl enable --now serial-getty@ttyS0.service
virsh pool-define-as lazylab dir - - - - "/var/lib/libvirt/images/lazylab"
virsh pool-build lazylab
virsh pool-start lazylab
virsh pool-autostart lazylab
