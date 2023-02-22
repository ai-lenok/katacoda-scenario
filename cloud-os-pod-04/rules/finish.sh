#!/bin/bash
PS1=1
source /root/.bashrc

function param {
    grep "$1" "/root/$2.env" | cut -d'=' -f2
}

# Проверка пода egress
EGRESS_POD=$(oc get pods -o name | grep egress | wc -l)
# Параметры Egress
EGRESS_NAME=$(param 'EGRESS_NAME' 'egress-params')
KAFKA_HOST=$(param 'HOST' 'connection')
KAFKA_PORT=$(param 'PORT' 'connection')
# Проверка вызовов
SIDECAR_LOG="$(oc logs $(oc get pods -o name | grep kafka-client | head -n 1) -c istio-proxy 2>&1 | grep $EGRESS_NAME | grep $KAFKA_PORT | wc -l)"
EGRESS_LOG="$(oc logs $(oc get pods -o name | grep egress | head -n 1) 2>&1 | grep $KAFKA_HOST | grep $KAFKA_PORT | wc -l)"
# Проверка конфигов Openshift
GW=$(oc describe gateways 2>&1 | grep ${KAFKA_HOST} | wc -l)
VS=$(oc describe virtualservices 2>&1 | grep ${KAFKA_HOST} | wc -l)
SE=$(oc describe serviceentry 2>&1 | grep ${KAFKA_HOST} | wc -l)

jq --null-input \
--arg EGRESS_POD "$EGRESS_POD" \
--arg SIDECAR_LOG "$SIDECAR_LOG" \
--arg EGRESS_LOG "$EGRESS_LOG" \
--arg GW "$GW" \
--arg VS "$VS" \
--arg SE "$SE" \
'{
    "log":{"sidecar": $SIDECAR_LOG,"egress": $EGRESS_LOG,},
    "egress": $EGRESS_POD,
    "gw": $GW,
    "vs": $VS,
    "se": $SE,
}'