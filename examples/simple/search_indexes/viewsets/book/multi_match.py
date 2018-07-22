from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    HighlightBackend,
    IdsFilterBackend,
    MultiMatchSearchFilterBackend,
    OrderingFilterBackend,
    PostFilterFilteringFilterBackend,
    SuggesterFilterBackend,
)

from .default import BookDocumentViewSet

__all__ = (
    'BookMultiMatchSearchFilterBackendDocumentViewSet',
)


class BookMultiMatchSearchFilterBackendDocumentViewSet(
    BookDocumentViewSet
):
    """Same as BookDocumentViewSet, but multi match."""

    filter_backends = [
        FilteringFilterBackend,
        PostFilterFilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        MultiMatchSearchFilterBackend,
        FacetedSearchFilterBackend,
        HighlightBackend,
        SuggesterFilterBackend,
    ]

    search_fields = {
        'title': None,
        'summary': None,
        'description': None,
    }
    ordering = ('_score', 'id', 'title', 'price',)

    multi_match_options = {
        'type': 'phrase',
    }
