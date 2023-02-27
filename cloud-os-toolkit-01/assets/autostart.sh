#!/bin/bash -x
PS1=1
source ~/.bashrc

DONE_FILE=/usr/local/etc/autostart.sh.done

oc apply -f /usr/local/prepare/python-config-map.yaml

touch $DONE_FILE