rm docs/*.rst
rm -rf builddocs/
sphinx-apidoc src/django_elasticsearch_dsl_drf --full -o docs -H 'django-elasticsearch-dsl-drf' -A 'Artur Barseghyan <artur.barseghyan@gmail.com>' -V '0.1' -f -d 20
cp docs/conf.distrib docs/conf.py
