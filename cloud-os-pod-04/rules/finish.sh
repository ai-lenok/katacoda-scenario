#!/bin/bash
PS1=1
source /root/.bashrc

#ADDRESS_BOOK_POD=$(oc get pods -o name | grep addressbook | wc -l)

printf "{\"Message\": \"FAIL: $(oc get pods -o name | grep addressbook | wc -l)\"}"

#jq --null-input \
#--arg ADDRESS_BOOK_POD "$ADDRESS_BOOK_POD" \
#--arg SIDECAR_LOG "$SIDECAR_LOG" \
#--arg EGRESS_LOG "$EGRESS_LOG" \
#--arg GW "$GW" \
#--arg VS "$VS" \
#--arg SE "$SE" \
#'{
#    "pod": $ADDRESS_BOOK_POD
#}'