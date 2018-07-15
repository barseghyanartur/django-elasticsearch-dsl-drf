===============
Search backends
===============

**Viewset**

.. code-block:: python




    class BaseDocumentViewSet(BaseDocumentViewSet):
        """Base BookDocument ViewSet."""

        document = BookDocument
        # serializer_class = BookDocumentSerializer
        serializer_class = BookDocumentSimpleSerializer
        lookup_field = 'id'
        filter_backends = [
            FilteringFilterBackend,
            PostFilterFilteringFilterBackend,
            IdsFilterBackend,
            OrderingFilterBackend,
            DefaultOrderingFilterBackend,
            SearchFilterBackend,
            FacetedSearchFilterBackend,
            # SuggesterFilterBackend,
            # FunctionalSuggesterFilterBackend,
            HighlightBackend,
        ]
        # Define search fields
        search_fields = (
            'title',
            'description',
            'summary',
        )

        search_nested_fields = {
            'country': ['name'],
        }

        search_filter_backend_queries = [
            MatchSearchQuery,
            MultiMatchSearchQuery,
            NestedSearchQuery,
        ]
