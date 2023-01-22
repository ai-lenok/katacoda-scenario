#!/usr/bin/env bash

if mvn verify &> /root/out.txt
then
  echo '{"result":"FAIL"}'
#  echo '{"result":"OK"}'
else
  echo '{"result":"FAIL"}'
fi