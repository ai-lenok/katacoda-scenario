#!/usr/bin/env bash

if cd /root; mvn test
then
  echo '{"result":"OK"}'
else
  echo '{"result":"FAIL"}'
fi