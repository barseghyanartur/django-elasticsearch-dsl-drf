from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_TERMS,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    SUGGESTER_COMPLETION,
    SUGGESTER_PHRASE,
    SUGGESTER_TERM,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    PostFilterFilteringFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import (
    BaseDocumentViewSet,
)

from elasticsearch_dsl import DateHistogramFacet, RangeFacet, A

from ..documents import JournalDocument
from ..serializers import JournalDocumentSerializer

__all__ = (
    'JournalDocumentViewSet',
)


class JournalDocumentViewSet(BaseDocumentViewSet):
    """JournalDocument ViewSet."""

    document = JournalDocument
    serializer_class = JournalDocumentSerializer
    lookup_field = 'isbn'
    document_uid_field = 'isbn.raw'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
        FacetedSearchFilterBackend,
        SuggesterFilterBackend,
    ]
    # Define search fields
    search_fields = (
        'title',
        'description',
        'summary',
    )
    # Define highlight fields
    highlight_fields = {
        'title': {
            'enabled': True,
            'options': {
                'pre_tags': ["<b>"],
                'post_tags': ["</b>"],
            }
        },
        'summary': {
            'options': {
                'fragment_size': 50,
                'number_of_fragments': 3
            }
        },
        'description': {},
    }
    # Define filter fields
    filter_fields = {
        'isbn': {
            'field': 'isbn',
            'lookups': [
                LOOKUP_QUERY_IN,
                LOOKUP_FILTER_TERMS,
            ],
        },
        'title': 'title.raw',
        'summary': 'summary',
        'publisher': 'publisher.raw',
        'publication_date': 'publication_date',
        'state': 'state.raw',
        'isbn_raw': 'isbn.raw',
        'price': {
            'field': 'price.raw',
            'lookups': [
                LOOKUP_FILTER_RANGE,
            ],
        },
        'pages': {
            'field': 'pages',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'stock_count': {
            # 'field': 'stock_count',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
    }
    # Define ordering fields
    ordering_fields = {
        'isbn': 'isbn.raw',
        'title': 'title.raw',
        'price': 'price',
        'publication_date': 'publication_date',
    }
    # Specify default ordering
    ordering = ('isbn.raw', 'title', 'price',)
    faceted_search_fields = {
        'pages_count': {
            'field': 'pages',
            'facet': RangeFacet,
            'options': {
                'ranges': [
                    ("<10", (None, 10)),
                    ("11-20", (11, 20)),
                    ("20-50", (20, 50)),
                    (">50", (50, None)),
                ]
            }
        },
        'price': {
            # 'field': 'price',
            'facet': RangeFacet,
            'options': {
                'ranges': [
                    ("<10", (None, 10)),
                    ("11-20", (11, 20)),
                    ("20-50", (20, 50)),
                    (">50", (50, None)),
                ]
            }
        },
        'price_metric_max': {
            "field": "price",
            'options': {
                'metric': A('max', field='price'),
            },
        },
    }
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
        'summary_suggest': 'summary',
    }
