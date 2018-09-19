from django_elasticsearch_dsl_drf.constants import (
    FUNCTIONAL_SUGGESTER_COMPLETION_MATCH,
    FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    FunctionalSuggesterFilterBackend,
    HighlightBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import (
    FunctionalSuggestMixin,
)

from .base import BaseBookDocumentViewSet

__all__ = (
    'BookFunctionalSuggesterDocumentViewSet',
)


class BookFunctionalSuggesterDocumentViewSet(BaseBookDocumentViewSet,
                                             FunctionalSuggestMixin):
    """Same as BookDocumentViewSet, but uses functional suggester."""

    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
        FacetedSearchFilterBackend,
        HighlightBackend,
        FunctionalSuggesterFilterBackend,
    ]

    # Functional suggester fields
    functional_suggester_fields = {
        'title_suggest_prefix': {
            'field': 'title.raw',
            'suggesters': [
                FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
                FUNCTIONAL_SUGGESTER_COMPLETION_MATCH,
            ],
            'default_suggester': FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
            'options': {
                'size': 100,
                'from': 0,
            }
            # 'serializer_field': 'title',
        },
        'title_suggest_match': {
            'field': 'title.edge_ngram_completion',
            'suggesters': [FUNCTIONAL_SUGGESTER_COMPLETION_MATCH],
            'default_suggester': FUNCTIONAL_SUGGESTER_COMPLETION_MATCH,
            # 'serializer_field': 'title',
        },
        'title.raw': None,
        'title_simple': 'title.raw',
        # 'publisher_suggest': 'publisher.raw',
        # 'tag_suggest': 'tags',
        # 'summary_suggest': 'summary',
    }
