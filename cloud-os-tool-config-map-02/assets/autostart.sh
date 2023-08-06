#!/bin/bash -x
PS1=1
source ~/.bashrc

DONE_FILE=/usr/local/etc/autostart.sh.done

oc apply --filename /usr/local/prepare/config-map-example.yaml

touch $DONE_FILE