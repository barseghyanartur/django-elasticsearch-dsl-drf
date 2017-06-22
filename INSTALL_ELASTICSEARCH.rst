Install Elasticsearch
=====================
Install Elasticsearch 2.x
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

Useful tools
------------

Once you have installed the Elasticsearch and indexed your haystack models,
you might want to be able to browse through the index.

The `official site
<https://www.elastic.co/guide/en/elasticsearch/client/community/current/front-ends.html>`_
mentions a couple of useful plugins. One of them is `elasticsearch-head
<http://mobz.github.io/elasticsearch-head/>`_.

Once you have installed the Elasticsearch itself, do the following (tested
on Ubuntu 14.04; might work on other platforms as well):

.. code-block:: sh

    sudo /usr/share/elasticsearch/bin/plugin install mobz/elasticsearch-head

Now open the `following <http://localhost:9200/_plugin/head/>`_ URL in your
browser.
