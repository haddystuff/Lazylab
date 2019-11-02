#!/bin/bash 
#this is initial script for lazylab. You need to run it as root before you can use lazylab

#Starting tty service for telnet console connection
systemctl enable --now serial-getty@ttyS0.service

#Creating new volume pool named "lazylab"
virsh pool-define-as lazylab dir - - - - "/var/lib/libvirt/images/lazylab"
virsh pool-build lazylab
virsh pool-start lazylab
virsh pool-autostart lazylab
