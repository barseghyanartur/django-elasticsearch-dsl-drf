#!/usr/bin/env bash
reset
#./scripts/uninstall.sh
#./scripts/install.sh
python examples/simple/manage.py test django_elasticsearch_dsl_drf.tests.test_suggesters --traceback -v 3 --settings=settings.testing
