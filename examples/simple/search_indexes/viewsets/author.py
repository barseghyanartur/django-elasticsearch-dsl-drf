from django_elasticsearch_dsl_drf.constants import (
    SUGGESTER_TERM,
    SUGGESTER_PHRASE,
    SUGGESTER_COMPLETION,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    DefaultOrderingFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.views import BaseDocumentViewSet

from ..documents import AuthorDocument
from ..serializers import AuthorDocumentSimpleSerializer

__all__ = (
    'AuthorDocumentViewSet',
)


class AuthorDocumentViewSet(BaseDocumentViewSet):
    """The AuthorDocument view."""

    document = AuthorDocument
    serializer_class = AuthorDocumentSimpleSerializer
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend,
    ]
    pagination_class = LimitOffsetPagination
    # Define search fields
    search_fields = (
        'name',
        'email',
        'salutation',
    )
    # Define filtering fields
    filter_fields = {
        'id': None,
        'name': 'name.raw',
    }
    # Define ordering fields
    ordering_fields = {
        'id': None,  # 'id',
        'name': 'name.raw',
        'email': 'email.raw',
        'salutation': 'salutation.raw',
    }
    # Specify default ordering
    ordering = 'name.raw'

    # Suggester fields
    suggester_fields = {
        'name_suggest': {
            'field': 'name.suggest',
            'suggesters': [
                SUGGESTER_TERM,
                SUGGESTER_PHRASE,
                SUGGESTER_COMPLETION,
            ],
        },
        'salutation.suggest': {
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
    }
