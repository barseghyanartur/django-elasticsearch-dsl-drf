Demo
====
Run demo locally
----------------
In order to be able to quickly evaluate the ``django-elasticsearch-dsl-drf``,
a demo app (with a quick installer) has been created (works on Ubuntu/Debian,
may work on other Linux systems as well, although not guaranteed). Follow the
instructions below for having the demo running within a minute.

Prerequisites
-------------
- Python 3
- Docker

Grab and run Elasticsearch:

.. code-block:: sh

    docker pull docker.elastic.co/elasticsearch/elasticsearch:5.5.3
    docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:5.5.3

Grab and run the latest ``django_elasticsearch_dsl_drf_demo_installer.sh``:

.. code-block:: sh

    wget -O - https://raw.github.com/barseghyanartur/django-elasticsearch-dsl-drf/stable/examples/django_elasticsearch_dsl_drf_demo_installer.sh | bash

Open your browser and test the app.

- URL: http://127.0.0.1:8001/search/
