#!/usr/bin/env bash

if mvn test
then
  echo "OK"
else
  echo "FAIL: unit test unsuccessful"
fi