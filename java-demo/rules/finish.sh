#!/usr/bin/env bash

if mvn test
then
  echo '{"result":"OK"}'
else
  echo '{"result":"FAIL"}'
fi