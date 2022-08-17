wget -O django_elasticsearch_dsl_drf_demo_installer.tar.gz https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/archive/master.tar.gz
virtualenv django-elasticsearch-dsl-drf-env
source django-elasticsearch-dsl-drf-env/bin/activate
mkdir django_elasticsearch_dsl_drf_demo_installer/
tar -xvf django_elasticsearch_dsl_drf_demo_installer.tar.gz -C django_elasticsearch_dsl_drf_demo_installer
cd django_elasticsearch_dsl_drf_demo_installer/django-elasticsearch-dsl-drf-stable/examples/simple/
pip install -r ../../requirements.txt
pip install https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/archive/master.tar.gz
mkdir ../media/
mkdir ../media/static/
mkdir ../static/
mkdir ../db/
mkdir ../logs/
mkdir ../tmp/
cp settings/local_settings.example settings/local_settings.py
./manage.py migrate --noinput --traceback -v 3
./manage.py collectstatic --noinput --traceback -v 3
./manage.py books_create_test_data --number=20 --traceback -v 3
./manage.py runserver 0.0.0.0:8001 --traceback -v 3
