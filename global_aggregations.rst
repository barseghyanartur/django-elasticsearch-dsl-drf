Global aggregations
===================
Global aggregations.

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

    http://localhost:8000/search/books/?publisher=Egmont

Sample response
---------------

.. code-block:: javascript

