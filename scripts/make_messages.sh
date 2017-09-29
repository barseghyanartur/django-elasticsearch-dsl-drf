#!/usr/bin/env bash
echo 'Making messages for django-elasticsearch-dsl-drf...'
cd src/django_elasticsearch_dsl_drf/
django-admin.py makemessages -l de
django-admin.py makemessages -l nl
django-admin.py makemessages -l ru

echo 'Making messages for example projects...'
cd ../../examples/simple/
django-admin.py makemessages -l de
django-admin.py makemessages -l nl
django-admin.py makemessages -l ru
