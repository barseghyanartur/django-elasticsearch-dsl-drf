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

from .multi_match import BookMultiMatchSearchFilterBackendDocumentViewSet

__all__ = (
    'BookMultiMatchOptionsPhasePrefixSearchFilterBackendDocumentViewSet',
)


class BookMultiMatchOptionsPhasePrefixSearchFilterBackendDocumentViewSet(
    BookMultiMatchSearchFilterBackendDocumentViewSet
):
    """Same as parent, but uses `multi_match_search_fields` declarations.

    Additionally, uses `phase_prefix`.
    """

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

    multi_match_search_fields = {
        'title': {'boost': 4},
        'summary': {'boost': 2},
        'description': None,
    }
    ordering = ('_score', 'id', 'title', 'price',)

    multi_match_options = {
        'type': 'phrase_prefix',
    }
