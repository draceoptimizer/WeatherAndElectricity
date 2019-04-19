#!/usr/bin/env bash
#Run the tests for Weather and Electricity code
pt_command="pytest --disable-pytest-warnings"
tests=("test_dark_sky_management.py")
for t in "${tests[@]}"
do
    command="${pt_command} ${t}"
    echo "RUNNING: ${command}"
    eval ${command}
done