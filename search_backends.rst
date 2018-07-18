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

        search_fields = (
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

        search_fields = {
            'title': {'boost': 4},
            'summary': {'boost': 2},
            'description': None,
        }

        ordering = ('_score', 'id', 'title', 'price',)

Sample request
~~~~~~~~~~~~~~
.. note::

    Multiple search params (`search_multi`) are not supported. Even if you
    provide multiple search params, the first one would be picked, having
    the rest simply ignored.

.. code-block:: text

    http://localhost:8000/search/books-multi-match-search-backend/?search_multi=debitis%20enim

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
