from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    HighlightBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    PostFilterFilteringFilterBackend,
    SuggesterFilterBackend,
)

from .default import BookDocumentViewSet

__all__ = (
    'BookOrderingByScoreCompoundSearchBackendDocumentViewSet',
)


class BookOrderingByScoreCompoundSearchBackendDocumentViewSet(
    BookDocumentViewSet
):
    """Same as BookDocumentViewSet, but sorted by _score."""

    filter_backends = [
        FilteringFilterBackend,
        PostFilterFilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
        FacetedSearchFilterBackend,
        HighlightBackend,
        SuggesterFilterBackend,
    ]

    search_fields = {
        'title': {'boost': 4},
        'summary': {'boost': 2},
        'description': None,
    }
    ordering = ('_score', 'id', 'title', 'price',)
