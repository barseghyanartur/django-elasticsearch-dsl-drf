===============
Search backends
===============
Compound search filter backend
------------------------------
Compound search filter backend aims to replace old style `SearchFilterBackend`.

Sample view
~~~~~~~~~~~

.. code-block:: python

    from django_elasticsearch_dsl_drf.filter_backends import (
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
        OrderingFilterBackend,
    )
    from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

    from .documents import BookDocument
    from .serializers import BookDocumentSerializer

    class BookCompoundSearchBackendDocumentViewSet(DocumentViewSet):

        document = BookDocument
        serializer_class = BookDocumentSerializer
        lookup_field = 'id'

        filter_backends = [
            # ...
            OrderingFilterBackend,
            DefaultOrderingFilterBackend,
            CompoundSearchFilterBackend,
            # ...
        ]

        multi_match_search_fields = (
            'title',
            'description',
            'summary',
        )

        ordering = ('_score', 'id', 'title', 'price',)

Sample request
~~~~~~~~~~~~~~

.. code-block:: text

    http://localhost:8000/search/books-compound-search-backend/?search=enim

Generated query
~~~~~~~~~~~~~~~

.. code-block:: javascript

    {
      "from": 0,
      "sort": [
        "id",
        "title",
        "price"
      ],
      "size": 23,
      "query": {
        "bool": {
          "should": [
            {
              "match": {
                "title": {
                  "query": "enim"
                }
              }
            },
            {
              "match": {
                "description": {
                  "query": "enim"
                }
              }
            },
            {
              "match": {
                "summary": {
                  "query": "enim"
                }
              }
            }
          ]
        }
      }
    }

Multi match search filter backend
---------------------------------
Document and serializer definition are trivial (there are lots of examples
in other sections).

Sample view
~~~~~~~~~~~

.. code-block:: python

    from django_elasticsearch_dsl_drf.filter_backends import (
        DefaultOrderingFilterBackend,
        MultiMatchSearchFilterBackend,
        OrderingFilterBackend,
    )
    from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

    from .documents import BookDocument
    from .serializers import BookDocumentSerializer


    class BookMultiMatchSearchFilterBackendDocumentViewSet(DocumentViewSet):

        document = BookDocument
        serializer_class = BookDocumentSerializer
        lookup_field = 'id'

        filter_backends = [
            # ...
            OrderingFilterBackend,
            DefaultOrderingFilterBackend,
            MultiMatchSearchFilterBackend,
            # ...
        ]

        multi_match_search_fields = {
            'title': {'boost': 4},
            'summary': {'boost': 2},
            'description': None,
        }

        ordering = ('_score', 'id', 'title', 'price',)

Sample request
~~~~~~~~~~~~~~
.. note::

    Multiple search params (`search_multi_match`) are not supported. Even if
    you provide multiple search params, the first one would be picked, having
    the rest simply ignored.

.. code-block:: text

    http://localhost:8000/search/books-multi-match-search-backend/?search_multi_match=debitis%20enim

Generated query
~~~~~~~~~~~~~~~

.. code-block:: javascript

    {
      "from": 0,
      "query": {
        "multi_match": {
          "query": "debitis enim",
          "fields": [
            "summary^2",
            "description",
            "title^4"
          ]
        }
      },
      "size": 38,
      "sort": [
        "_score",
        "id",
        "title",
        "price"
      ]
    }

Options
~~~~~~~
All standard multi match query options are available/tunable with help of
``multi_match_options`` view property.

Selective list of available options:

- operator
- type
- analyzer
- tie_breaker

Type options
^^^^^^^^^^^^

See the `Elasticsearch docs
<https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html#type-phrase>`_
for detailed explanation.

- best_fields
- most_fields
- cross_fields
- phrase
- phrase_prefix

**Example**

.. code-block:: python

    class BookMultiMatchSearchFilterBackendDocumentViewSet(DocumentViewSet):

        # ...

        multi_match_options = {
            'type': 'phrase'
        }

Operator options
^^^^^^^^^^^^^^^^
Can be either ``and`` or ``or``.

Simple query string filter backend
----------------------------------
Document and serializer definition are trivial (there are lots of examples
in other sections).

Sample view
~~~~~~~~~~~

.. code-block:: python

    from django_elasticsearch_dsl_drf.filter_backends import (
        DefaultOrderingFilterBackend,
        SimpleQueryStringSearchFilterBackend,
        OrderingFilterBackend,
    )
    from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

    from .documents import BookDocument
    from .serializers import BookDocumentSerializer


    class BookSimpleQueryStringSearchFilterBackendDocumentViewSet(DocumentViewSet):

        document = BookDocument
        serializer_class = BookDocumentSerializer
        lookup_field = 'id'

        filter_backends = [
            # ...
            OrderingFilterBackend,
            DefaultOrderingFilterBackend,
            SimpleQueryStringSearchFilterBackend,
            # ...
        ]

        simple_query_string_search_fields = {
            'title': {'boost': 4},
            'summary': {'boost': 2},
            'description': None,
        }

        ordering = ('_score', 'id', 'title', 'price',)

Sample request 1
~~~~~~~~~~~~~~~~
.. note::

    Multiple search params (`search_simple_query_string`) are not supported.
    Even if you provide multiple search params, the first one would be picked,
    having the rest simply ignored.

.. code-block:: text

    http://localhost:8000/search/books-simple-query-string-search-backend/?search_simple_query_string="chapter%20II"%20%2Bfender

Generated query 1
~~~~~~~~~~~~~~~~~

.. code-block:: javascript

    {
      "query": {
        "simple_query_string": {
          "query": "\"chapter II\" +fender",
          "default_operator": "and",
          "fields": [
            "title",
            "description",
            "summary"
          ]
        }
      },
      "sort": [
        "_score",
        "id",
        "title",
        "price"
      ],
      "from": 0,
      "size": 1
    }

Sample request 2
~~~~~~~~~~~~~~~~
.. note::

    Multiple search params (`search_simple_query_string`) are not supported.
    Even if you provide multiple search params, the first one would be picked,
    having the rest simply ignored.

.. code-block:: text

    http://localhost:8000/search/books-simple-query-string-search-backend/?search_simple_query_string="chapter%20II"%20%2B(shutting%20|%20fender)

Generated query 2
~~~~~~~~~~~~~~~~~

.. code-block:: javascript

    {
      "query": {
        "simple_query_string": {
          "query": "\"chapter II\" +(shutting | fender)",
          "default_operator": "and",
          "fields": [
            "title",
            "description",
            "summary"
          ]
        }
      },
      "sort": [
        "_score",
        "id",
        "title",
        "price"
      ],
      "from": 0,
      "size": 2
    }


Sample request 3
~~~~~~~~~~~~~~~~
.. note::

    Multiple search params (`search_simple_query_string`) are not supported.
    Even if you provide multiple search params, the first one would be picked,
    having the rest simply ignored.

.. code-block:: text

    http://localhost:8000/search/books-simple-query-string-search-backend/?search_simple_query_string=%22Pool%20of%20Tears%22%20-considering

Generated query 3
~~~~~~~~~~~~~~~~~

.. code-block:: javascript

    {
      "query": {
        "simple_query_string": {
          "query": "\"Pool of Tears\" -considering",
          "default_operator": "and",
          "fields": [
            "title",
            "description",
            "summary"
          ]
        }
      },
      "sort": [
        "_score",
        "id",
        "title",
        "price"
      ],
      "from": 0,
      "size": 1
    }

Options
~~~~~~~
All standard multi match query options are available/tunable with help of
``simple_query_string_options`` view property.

Selective list of available options:

- default_operator

Default Operator options
^^^^^^^^^^^^^^^^^^^^^^^^
Can be either ``and`` or ``or``.

**Example**

.. code-block:: python

    class BookSimpleQueryStringSearchFilterBackendDocumentViewSet(DocumentViewSet):

        # ...

        simple_query_string_options = {
            "default_operator": "and",
        }
