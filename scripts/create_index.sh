#!/usr/bin/env bash
cd examples/simple/
./manage.py search_index --create -f
./manage.py search_index --populate -f
