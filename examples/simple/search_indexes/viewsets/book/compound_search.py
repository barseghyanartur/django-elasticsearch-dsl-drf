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
    'BookCompoundFuzzySearchBackendDocumentViewSet',
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


class BookCompoundFuzzySearchBackendDocumentViewSet(BookDocumentViewSet):
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

    search_fields = {
        'title': {'fuzziness': 'AUTO'},
        'description': None,
        'summary': None,
    }
