#!/usr/bin/env bash
pip uninstall django-elasticsearch-dsl-drf -y
rm build -rf
rm dist -rf
rm -rf src/django_elasticsearch_dsl_drf.egg-info
rm -rf src/django-elasticsearch-dsl-drf.egg-info
rm builddocs.zip
rm builddocs/ -rf
