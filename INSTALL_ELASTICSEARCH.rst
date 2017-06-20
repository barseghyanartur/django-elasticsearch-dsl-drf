Install ElasticSearch
=====================
Install ElasticSearch 2.x
-------------------------
(1) First, update your package index.

    .. code-block:: sh

        sudo apt-get update

(2) Download the latest Elasticsearch version, which is 2.4.5 at the time of
    writing.

    .. code-block:: sh

        wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.4.5/elasticsearch-2.4.5.deb

(3) Then install it in the usual Ubuntu way with dpkg.

    .. code-block:: sh

        sudo dpkg -i elasticsearch-2.4.5.deb
