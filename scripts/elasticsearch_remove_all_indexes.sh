#!/usr/bin/env bash
cd examples/simple/
./manage.py elasticsearch_remove_indexes --with-protected --settings=settings.dev "$@"
