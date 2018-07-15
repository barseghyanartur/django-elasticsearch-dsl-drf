Installing Elasticsearch
========================
For development and testing purposes, it's often handy to be able to
quickly switch between different Elasticsearch versions. Since this packages
supports 2.x, 5.x (and in nearest future - 6.x) branches, you could make use of
the following boxes/containers for development and testing.

For all containers/boxes mentioned below, no authentication is required (for
Elasticsearch).

Docker
------
5.x
~~~
.. code-block:: sh

    docker pull docker.elastic.co/elasticsearch/elasticsearch:5.5.3
    docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:5.5.3

6.x
~~~
.. code-block:: sh

    docker pull docker.elastic.co/elasticsearch/elasticsearch:6.3.0
    docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:6.3.0

Vagrant
-------
2.x
~~~

.. code-block:: sh

    ./scripts/vagrant_start.sh
