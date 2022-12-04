#!/bin/bash

cat << EOF
{
    "script01": "OK",
    "script02": "FAIL: File or directory does not exist: _file_name_",
    "script03": "FAIL: I found the wrong text: _word_",
    "script04": "FAIL: The filename is incorrect: _file_name_"
}
EOF
