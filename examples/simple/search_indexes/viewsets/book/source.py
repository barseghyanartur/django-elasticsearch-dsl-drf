from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    HighlightBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    PostFilterFilteringFilterBackend,
    SourceBackend,
    SuggesterFilterBackend,
)

from .default import BookDocumentViewSet
from ...serializers.book import BookDocumentSourceSerializer

__all__ = (
    'BookSourceSearchBackendDocumentViewSet',
)


class BookSourceSearchBackendDocumentViewSet(BookDocumentViewSet):
    """Book document view set based on compound search backend using source."""

    filter_backends = [
        SourceBackend,
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

    serializer_class = BookDocumentSourceSerializer

    source = [
        "id",
        "title",
    ]
