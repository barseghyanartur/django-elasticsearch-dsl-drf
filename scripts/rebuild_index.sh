#!/usr/bin/env bash
cd examples/simple/
./manage.py search_index --rebuild -f --settings=settings.dev "$@"
./manage.py opensearch --settings=settings.dev "$@" index rebuild --force
