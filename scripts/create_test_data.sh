#!/usr/bin/env bash
cd examples/simple/
./manage.py books_create_test_data --traceback -v 3 "$@"
