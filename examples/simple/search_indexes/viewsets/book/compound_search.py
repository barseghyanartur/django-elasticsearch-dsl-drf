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
    'BookCompoundSearchBackendDocumentViewSet',
)


class BookCompoundSearchBackendDocumentViewSet(BookDocumentViewSet):
    """Book document view set based on compound search backend."""

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
