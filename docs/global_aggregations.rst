Global aggregations
===================
Global aggregations (facets) are regular aggregations, which are not influenced
by the search query/filter. They deliver results similar to `post_filter`.

Sample view
-----------

.. code-block:: python

    from django_elasticsearch_dsl_drf.filter_backends import (
        CompoundSearchFilterBackend,
        DefaultOrderingFilterBackend,
        FacetedSearchFilterBackend,
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
            FacetedSearchFilterBackend,
            # ...
        ]

        faceted_search_fields = {
            'publisher': {
                'field': 'publisher.raw',
                'enabled': True,
                'global': True,  # This makes the aggregation global
            },
        }

Sample request
--------------

.. code-block:: text

    http://localhost:8000/search/books/?facet=state_global&state=rejected

Generated query
---------------

.. code-block:: javascript
    {
       "from":0,
       "query":{
          "bool":{
             "filter":[
                {
                   "terms":{
                      "state.raw":[
                         "rejected"
                      ]
                   }
                }
             ]
          }
       },
       "size":25,
       "aggs":{
          "_filter_state_global":{
             "aggs":{
                "state_global":{
                   "terms":{
                      "field":"state.raw"
                   }
                }
             },
             "global":{

             }
          }
       },
       "sort":[
          "id",
          "title",
          "price"
       ]
    }

Sample response
---------------

.. code-block:: javascript

    {
        "count": 25,
        "next": null,
        "previous": null,
        "facets": {
            "_filter_state_global": {
                "state_global": {
                    "buckets": [
                        {
                            "doc_count": 29,
                            "key": "not_published"
                        },
                        {
                            "doc_count": 25,
                            "key": "in_progress"
                        },
                        {
                            "doc_count": 25,
                            "key": "rejected"
                        },
                        {
                            "doc_count": 21,
                            "key": "cancelled"
                        },
                        {
                            "doc_count": 17,
                            "key": "published"
                        }
                    ],
                    "sum_other_doc_count": 0,
                    "doc_count_error_upper_bound": 0
                },
                "doc_count": 117
            }
        },
        "results": [
            {
                "id": 1007489,
                "title": "Cupiditate qui nulla itaque maxime impedit.",
                "description": null,
                "summary": "Aut recusandae architecto incidunt quaerat odio .",
                "authors": [
                    "Evy Vermeulen",
                    "Tycho Weijland",
                    "Rik Zeldenrust"
                ],
                "publisher": "Overdijk Inc",
                "publication_date": "2014-02-28",
                "state": "rejected",
                "isbn": "978-0-15-184366-4",
                "price": 6.53,
                "pages": 82,
                "stock_count": 30,
                "tags": [
                    "Trilogy"
                ],
                "highlight": {},
                "null_field": null,
                "score": null
            },
            # ...
        ]
    }
