#!/usr/bin/env bash

if mvn verify
then
  echo "OK"
else
  echo "FAIL"
fi