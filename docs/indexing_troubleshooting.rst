Indexing troubleshooting
========================
When indexing lots of data (millions of records), you might get timeout
exceptions.

A couple of possible solutions (complimentary) are listed below. All of them
are independent and not strictly related to each other. Thus, you may just use
one or a couple or all of them. It's totally up to you.

Timeout
-------
For re-indexing, you might want to increase the timeout to avoid time-out
exceptions.

To do that, make a new settings file (`indexing`) and add the following:

*settings/indexing.py*

.. code-block:: python

    from .base import *  # Import from your main/production settings.

    # Override the elasticsearch configuration and provide a custom timeout
    ELASTICSEARCH_DSL = {
        'default': {
            'hosts': 'localhost:9200',
            'timeout': 60,  # Custom timeout
        },
    }

Then rebuild your search index specifying the indexing settings:

.. code-block:: sh

    ./manage.py search_index --rebuild -f --settings=settings.indexing

Note, that you may as well specify the timeout in your global settings.
However, if you're happy with how things work in production (except for the
indexing part), you may do as suggested (separate indexing settings).

Chunk size
----------
Note, that this feature is (yet) *only available in the forked version*
`barseghyanartur/django-elasticsearch-dsl
<https://github.com/barseghyanartur/django-elasticsearch-dsl/tree/mjl-index-speedup-2-additions>`_.

Install it as follows:

.. code-block:: sh

    pip install https://github.com/barseghyanartur/django-elasticsearch-dsl/archive/mjl-index-speedup-2-additions.zip

Specify the `chunk_size` param as follows (we set chunk_size to 50 in
this case):

.. code-block:: sh

    ./manage.py search_index --rebuild -f --chunk-size=50

Use parallel indexing
---------------------
Parallel indexing speeds things up (drastically). In my tests I got a speedup
boost of 66 percent on 1.6 million records.

Note, that this feature is (yet) *only available in the forked versions*
`barseghyanartur/django-elasticsearch-dsl
<https://github.com/barseghyanartur/django-elasticsearch-dsl/tree/mjl-index-speedup-2-additions>`_.
or
`mjl/django-elasticsearch-dsl <https://github.com/mjl/django-elasticsearch-dsl/tree/mjl-index-speedup>`_.

Install it as follows:

*barseghyanartur/django-elasticsearch-dsl fork*

.. code-block:: sh

    pip install https://github.com/barseghyanartur/django-elasticsearch-dsl/archive/mjl-index-speedup-2-additions.zip

*mjl/django-elasticsearch-dsl fork*

.. code-block:: sh

    pip install https://github.com/mjl/django-elasticsearch-dsl/archive/mjl-index-speedup.zip

In order to make use of it, define set `parallel_indexing` to True on the
document meta.

*yourapp/documents.py*

.. code-block:: python

    class LocationDocument(DocType):

        # ...

        class Meta(object):
            """Meta options."""

            model = Location
            parallel_indexing = True

Limit the number of items indexed at once
-----------------------------------------
This is very close to the `chunk_size` shown above, but might work better
on heavy querysets. Instead of processing entire queryset at once, it's
sliced instead. So, if you have 2 million records in your queryset and you
wish to index them by chunks of 20 thousands at once, specify the
`queryset_pagination` on the document meta:

*yourapp/documents.py*

.. code-block:: python

    class LocationDocument(DocType):

        # ...

        class Meta(object):
            """Meta options."""

            model = Location
            queryset_pagination = 50

You may even make it dynamic based on the settings loaded. So, for instance,
you may have it set to None in production (if you were happy with how things
were) and provide a certain value for it in the dedicated indexing
settings (as already has been mentioned above).

*settings/base.py*

.. code-block:: python

    # Main/production settings
    ELASTICSEARCH_DSL_QUERYSET_PAGINATION = None

*settings/indexing.py*

.. code-block:: python

    # Indexing only settings
    ELASTICSEARCH_DSL_QUERYSET_PAGINATION = 1000

*yourapp/documents.py*

.. code-block:: python

    from django.conf import settings

    # ...

    class LocationDocument(DocType):

        # ...

        class Meta(object):
            """Meta options."""

            model = Location
            queryset_pagination = settings.ELASTICSEARCH_DSL_QUERYSET_PAGINATION
