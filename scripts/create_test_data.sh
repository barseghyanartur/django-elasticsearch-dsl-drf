#!/usr/bin/env bash
cd examples/simple/
./manage.py books_create_test_data --number=100 --traceback -v 3
