#!/bin/bash -x

usermod \
--append \
  --groups docker \
ubuntu

docker run --name cont hello-world

DONE_FILE=/usr/local/etc/autostart.sh.done
touch $DONE_FILE