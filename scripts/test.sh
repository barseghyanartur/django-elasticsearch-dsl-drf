reset
#./scripts/uninstall.sh
#./scripts/install.sh
python examples/simple/manage.py test django_elasticsearch_dsl_drf --traceback -v 3 --settings=settings.testing
