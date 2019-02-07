from django.utils.decorators import classonlymethod
from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_EXCLUDE,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_ISNULL,
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
    HighlightBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    PostFilterFilteringFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
    FunctionalSuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import (
    DocumentViewSet,
)
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination

from elasticsearch_dsl import DateHistogramFacet, RangeFacet

from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission
from ...documents import BookDocument
from ...serializers import BookDocumentSimpleSerializer

__all__ = (
    'BookPermissionsDocumentViewSet',
)


class CustomPermission(BasePermission):

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return False


class CustomPageNumberPagination(PageNumberPagination):
    """This is needed in order to make page size customisation possible."""

    page_size_query_param = 'page_size'


class BookPermissionsDocumentViewSet(DocumentViewSet):
    """BookDocument permissions ViewSet.

    From the name you can guess that it's all about React frontend demo.
    """

    document = BookDocument
    serializer_class = BookDocumentSimpleSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (CustomPermission,)
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
        FacetedSearchFilterBackend,
        PostFilterFilteringFilterBackend,
        HighlightBackend,
        SuggesterFilterBackend,
        FunctionalSuggesterFilterBackend,
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
        'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
                LOOKUP_FILTER_TERMS,
            ],
        },
        'title': 'title.raw',
        'summary': 'summary',
        'publisher': 'publisher.raw',
        'publication_date_f': 'publication_date',
        'status': 'state.raw',
        'isbn': 'isbn.raw',
        'price_f': {
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
        'tags': {
            'field': 'tags',
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
                LOOKUP_QUERY_ISNULL,
            ],
        },
        'tags.raw': {
            'field': 'tags.raw',
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },
    }
    # Post filter fields, copy filters as they are valid
    post_filter_fields = {
        'publisher_pf': 'publisher.raw',
        'status_pf': 'state.raw',
        'price': 'price',
        'publication_date': {
            'field': 'publication_date',
        },
        'tags_pf': {
            'field': 'tags',
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
                LOOKUP_QUERY_ISNULL,
            ],
        },
        'tags.raw_pf': {
            'field': 'tags.raw',
            'lookups': [
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_EXCLUDE,
            ],
        },
    }
    # Define ordering fields
    ordering_fields = {
        'id': 'id',
        'title': 'title.raw',
        'price': 'price.raw',
        'state': 'state.raw',
        'publication_date': 'publication_date',
    }
    # Specify default ordering
    ordering = ('_score', 'id', 'title', 'price',)
    faceted_search_fields = {
        'status': {
            'field': 'state.raw',
            'enabled': True,
            # 'global': True,
            'options': {
                "min_doc_count": 0,
                "size": 20000,
                "order": {
                    "_term": "asc"
                },
            },
        },
        'publisher': {
            'field': 'publisher.raw',
            'enabled': True,
            # 'global': True,
            'options': {
                "min_doc_count": 0,
                "size": 20000,
                "order": {
                    "_term": "asc"
                },
            },
        },
        'publication_date': {
            'field': 'publication_date',
            'facet': DateHistogramFacet,
            # 'global': True,
            'enabled': True,
            'options': {
                'interval': 'year',
            },
        },
        'pages_count': {
            'field': 'pages',
            'facet': RangeFacet,
            'options': {
                'ranges': [
                    ("0__10", (0, 10)),
                    ("11__20", (11, 20)),
                    ("20__50", (20, 50)),
                    ("50__999999", (50, 999999)),
                ],
            }
        },
        'price': {
            # 'field': 'price',
            'facet': RangeFacet,
            'enabled': True,
            'options': {
                'ranges': [
                    ("0__9.99", (0, 9.99)),
                    ("10__19.99", (10, 19.99)),
                    ("20__49.99", (20, 49.99)),
                    ("50__999999", (50, 999999)),
                ],
            },
        },
    }
    # Suggester fields
    suggester_fields = {
        'title_suggest': {
            'field': 'title.suggest',
            'default_suggester': SUGGESTER_COMPLETION,
            'options': {
                'size': 20,
            },
        },
        'title_suggest_context': {
            'field': 'title.suggest_context',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
            'default_suggester': SUGGESTER_COMPLETION,
            # We want to be able to filter the completion filter
            # results on the following params: tag, state and publisher.
            # We also want to provide the size value.
            # See the "https://www.elastic.co/guide/en/elasticsearch/
            # reference/6.1/suggester-context.html" for the reference.
            'completion_options': {
                'category_filters': {
                    'title_suggest_tag': 'tag',
                    'title_suggest_state': 'state',
                    'title_suggest_publisher': 'publisher',
                },
            },
            'options': {
                'size': 20,
            },
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
