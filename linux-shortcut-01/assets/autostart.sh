#!/bin/bash -x

useradd remote_user

yes "changeme" | passwd remote_user

DONE_FILE=/usr/local/etc/autostart.sh.done
touch $DONE_FILE