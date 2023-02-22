#!/usr/bin/env bash

printf '{"Message": "FAIL: %s"}' $(oc get pods)