#!/bin/bash -x
#PS1=1
#source ~/.bashrc

DONE_FILE=/usr/local/etc/autostart.sh.done

docker run -d --net=host --name=prometheus \
   -v /root/prometheus.yml:/etc/prometheus/prometheus.yml \
   prom/prometheus \
   --config.file=/etc/prometheus/prometheus.yml \
   --storage.tsdb.path=/prometheus \
   --web.console.libraries=/usr/share/prometheus/console_libraries \
   --web.console.templates=/usr/share/prometheus/consoles \
   --web.route-prefix=$(cat /usr/local/etc/sbercode-prefix)-9090/ \
   --web.external-url=http://127.0.0.1/$(cat /usr/local/etc/sbercode-prefix)-9090/

touch $DONE_FILE