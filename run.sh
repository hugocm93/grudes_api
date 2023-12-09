#!/bin/bash

set -e

if [ "$1" == "test" ]; then
    pytest -v ./ML/test_model.py
elif [ "$1" == "debug" ]; then
    flask run --host 0.0.0.0 --port 5001 --reload 
else
    flask run --host 0.0.0.0 --port 5001
fi
