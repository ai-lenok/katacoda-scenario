#!/usr/bin/env bash

printf '{"Message": "FAIL": "%s"}' $(oc get pods)
#printf '{'Message': "FAIL: '%s'}" $(oc get pods)
#echo '{' '"Message"' ':' '"FAIL:"' '"' $(date) '"' '}'