Installing Elasticsearch
========================
For development and testing purposes, it's often handy to be able to
quickly switch between different Elasticsearch versions. Since this packages
supports 2.x, 5.x and 6.x branches, you could make use of
the following boxes/containers for development and testing.

For all containers/boxes mentioned below, no authentication is required (for
Elasticsearch).

Docker
------
2.x
~~~

.. code-block:: sh

    docker pull elasticsearch:2.4.6
    docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" elasticsearch:2.4.6

5.x
~~~
.. code-block:: sh

    docker pull docker.elastic.co/elasticsearch/elasticsearch:5.5.3
    docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:5.5.3

6.x
~~~
**6.3.2**

.. code-block:: sh

    docker pull docker.elastic.co/elasticsearch/elasticsearch:6.3.2
    docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:6.3.2

**6.4.0**

.. code-block:: sh

    docker pull docker.elastic.co/elasticsearch/elasticsearch:6.4.0
    docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:6.4.0

7.x
~~~
**7.1.1**

.. code-block:: sh

    docker pull docker.elastic.co/elasticsearch/elasticsearch:7.1.1
    docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:7.1.1

Vagrant
-------
2.x
~~~

.. code-block:: sh

    ./scripts/vagrant_start.sh
