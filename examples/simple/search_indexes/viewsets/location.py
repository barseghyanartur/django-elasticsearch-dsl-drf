from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_EXCLUDE,
    LOOKUP_QUERY_ISNULL,
    SUGGESTER_COMPLETION,
    SUGGESTER_PHRASE,
    SUGGESTER_TERM,
    FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
)
from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
    CompoundSearchFilterBackend,
    SuggesterFilterBackend,
    FunctionalSuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from ..documents import LocationDocument
from ..serializers import LocationDocumentSerializer


class LocationDocumentViewSet(DocumentViewSet):
    """
    Location Document View
    """
    document = LocationDocument
    serializer_class = LocationDocumentSerializer
    lookup_field = "slug"
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
        SuggesterFilterBackend,
        FunctionalSuggesterFilterBackend,
    ]
    # Define search fields
    search_fields = {
        "full": None,
        "full.q": None,
        "partial.q": None,
        "partial": None,
        "postcode": None,
    }
    # Define filter fields
    filter_fields = {
        "category": {
            "field": "category.raw",
            "lookups": [
                LOOKUP_FILTER_TERMS,
            ]
        },
        "occupied": {
            "field": "occupied.raw",
            "lookups": [
                LOOKUP_FILTER_TERMS,
            ]
        },
        "size": {
            "field": "size",
            "lookups": [
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LTE,
            ],
        },
        "staff": {
            "field": "staff",
            "lookups": [
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LTE,
            ],
        },
        "rent": {
            "field": "rent",
            "lookups": [
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LTE,
            ],
        },
        "revenue": {
            "field": "revenue",
            "lookups": [
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LTE,
            ],
        }
    }
    ordering_fields = {
        "full": "full.raw",
        "postcode": "postcode.raw"
    }

    # Functional suggester fields
    functional_suggester_fields = {
        "postcode": {
            "field": "postcode.raw",
            "suggesters": [FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX],
            "default_suggester": FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
            "options": {
                "size": 4,  # By default, number of results is 5.
            },
        },
    }

    # Specify default ordering
    ordering = ("_score",) # "full", "postcode",)
    suggester_fields = {
        "full": {
            "field": "full.suggest",
            "default_suggester": SUGGESTER_COMPLETION,
            "options": {
                'size': 4,  # By default, number of results is 5.
            },
        },
        "partial": {
            "field": "partial.suggest",
            "default_suggester": SUGGESTER_COMPLETION,
            "options": {
                'size': 10,  # By default, number of results is 5.
            },
        },
        "postcode": {
            "field": "postcode.suggest",
            "default_suggester": SUGGESTER_COMPLETION,
            "options": {
                'size': 10,  # By default, number of results is 5.
            },
        },
        "full_context": {
            "field": "full.context",
            "default_suggester": SUGGESTER_COMPLETION,
            "completion_options": {
                "category_filters": {
                    "fc": "category",
                    "fo": "occupied",
                },
            },
            "options": {
                'size': 4,  # By default, number of results is 5.
            },
        },
        "partial_context": {
            "field": "partial.context",
            "default_suggester": SUGGESTER_COMPLETION,
            "completion_options": {
                "category_filters": {
                    "rc": "category",
                    "ro": "occupied",
                },
            },
            "options": {
                'size': 10,  # By default, number of results is 5.
            },
        },
        "postcode_context": {
            "field": "postcode.context",
            "default_suggester": SUGGESTER_COMPLETION,
            "completion_options": {
                "category_filters": {
                    "pc": "category",
                    "po": "occupied",
                },
            },
            "options": {
                'size': 10,  # By default, number of results is 5.
            },
        },
    }
