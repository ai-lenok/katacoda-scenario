#!/usr/bin/env bash

if mvn verify &> /dev/null
then
  echo '{"result":"OK"}'
else
  echo '{"result":"FAIL: BUILD FAILURE"}'
fi