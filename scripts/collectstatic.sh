#!/usr/bin/env bash
cd examples/simple/
./manage.py collectstatic --noinput --settings=settings.dev "$@"
