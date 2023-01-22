#!/usr/bin/env bash

if pwd >> /root/out.txt ; ls -lah >> /root/out.txt
then
  echo '{"result":"OK"}'
else
  echo '{"result":"FAIL"}'
fi