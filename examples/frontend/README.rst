==============================================
frontend demo for django-elasticsearch-dsl-drf
==============================================
Frontend demo for django-elasticsearch-dsl-drf

Based on `Book
<https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/blob/master/examples/simple/books/models/book.py>`_
model, `BookDocument
<https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/blob/master/examples/simple/search_indexes/documents/book.py>`_
and `BookFrontendDocumentViewSet
<https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/blob/master/examples/simple/search_indexes/viewsets/book/frontend.py>`_
viewset.

Quick start
===========
From the project root directory.

Install the django requirements
-------------------------------
Since project supports Django versions from 1.8 to 2.1, you may install
any version you want.

To install latest LTS version, do:

.. code-block:: sh

    pip install -r examples/requirements/django_1_11.txt

Install Elasticsearch requirements
----------------------------------
Since project supports Elasticsearch versions from 2.x to 6.x, you may install
any version you want.

To install requirements for 6.x, do:

.. code-block:: sh

    pip install -r examples/requirements/elastic_6x.txt

Run Elasticsearch
-----------------
It's really easy using Docker.

To run 6.3.2 using Docker, do:

.. code-block:: sh

    docker pull docker.elastic.co/elasticsearch/elasticsearch:6.3.2
    docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:6.3.2

Build Elasticsearch index
-------------------------
First, create some test data:

.. code-block:: sh

    ./scripts/create_test_data.sh

Then build Elasticsearch index:

.. code-block:: sh

    ./scripts/rebuild_index.sh

Install React requirements
--------------------------
Note, that you should be using NodeJS > 7.5.

Typically, you would first do:

.. code-block:: sh

    nvm use 9

Then run the installer:

.. code-block:: sh

    ./scripts/yarn_install.sh

Run Django
----------
The following script would run the Django server which is used by the demo
app.

.. code-block:: sh

    ./scripts/runserver.sh

Run React demo app
------------------
Finally, run the React demo app:

.. code-block:: sh

    ./scripts/frontend.sh

Open `http://localhost:3000 <http://localhost:3000>`_ to view the frontend in
the browser.
