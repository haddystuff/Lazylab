#!/bin/bash 
#this is initial script for lazylab. You need to run it as root before you can use lazylab

#Add lazylab user
#adduser lazylab -M -c 'system user for lazylab script'

#Starting tty service for telnet console connection
systemctl enable --now serial-getty@ttyS0.service

#Creating new volume pool named "lazylab"
virsh pool-define-as lazylab dir - - - - "/var/lib/libvirt/images/lazylab"
virsh pool-build lazylab
virsh pool-start lazylab
virsh pool-autostart lazylab

# Changing permissions of volume pool(we do it just for developers)
chmod 777 /var/lib/libvirt/images/lazylab

#Getting dir files location
#DIR="$echo "`dirname "$0"`/*""
#MAIN_SCRIPT="$echo "`dirname "$0"`/lazylab.py""

#Changing own
#chown lazylab:lazylab $DIR

#Adding ssid
#chmod +s $MAIN_SCRIPT

#Change pool own
#chown lazylab:lazylab /var/lib/libvirt/images/lazylab
