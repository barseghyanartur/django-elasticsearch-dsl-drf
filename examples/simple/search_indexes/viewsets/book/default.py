from django_elasticsearch_dsl_drf.constants import (
    SUGGESTER_COMPLETION,
    SUGGESTER_PHRASE,
    SUGGESTER_TERM,

)
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    HighlightBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    PostFilterFilteringFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import (
    SuggestMixin,
    MoreLikeThisMixin,
)

from .base import BaseBookDocumentViewSet


__all__ = (
    'BookDocumentViewSet',
)


class BookDocumentViewSet(BaseBookDocumentViewSet,
                          SuggestMixin,
                          MoreLikeThisMixin):
    """The BookDocument view."""

    filter_backends = [
        FilteringFilterBackend,
        PostFilterFilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
        FacetedSearchFilterBackend,
        HighlightBackend,
        SuggesterFilterBackend,
    ]

    # Suggester fields
    suggester_fields = {
        'title_suggest': {
            'field': 'title.suggest',
            'default_suggester': SUGGESTER_COMPLETION,
        },
        'title_suggest_edge_ngram': {
            'field': 'title.edge_ngram_completion',
            'default_suggester': SUGGESTER_TERM,
            'suggesters': [
                SUGGESTER_PHRASE,
                SUGGESTER_TERM,
            ],
        },
        'title_suggest_mlt': {
            'field': 'title.mlt',
            'default_suggester': SUGGESTER_TERM,
            'suggesters': [
                SUGGESTER_PHRASE,
                SUGGESTER_TERM,
            ],
        },
        'publisher_suggest': 'publisher.suggest',
        'tag_suggest': 'tags.suggest',
        'summary_suggest': 'summary',
    }
