#!/usr/bin/env bash
cp examples/simple/settings/__init__.example examples/simple/settings/__init__.py
cp examples/simple/settings/local_settings.example examples/simple/settings/local_settings.py

mkdir -p examples/db
mkdir -p examples/logs

cd examples/simple

./manage.py migrate

./manage.py books_create_test_data --number=10
