from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_TERM,
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_EXCLUDE,
    LOOKUP_QUERY_IN,
)

from .default import BookDocumentViewSet

__all__ = (
    'BookDefaultFilterLookupDocumentViewSet',
)


class BookDefaultFilterLookupDocumentViewSet(BookDocumentViewSet):
    """Same as parent, but with default filter lookups & no default facets."""

    filter_fields = {
        'authors': {
            'field': 'authors.raw',
            'lookups': [
                LOOKUP_FILTER_TERM,
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
            'default_lookup': LOOKUP_FILTER_TERM,
        },
        'publisher': 'publisher.raw',
    }

    faceted_search_fields = {
        'state': 'state.raw',
        'publisher': {
            'field': 'publisher.raw',
            'enabled': False,
        },
    }
