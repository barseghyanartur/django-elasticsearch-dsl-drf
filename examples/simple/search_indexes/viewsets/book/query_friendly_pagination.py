from django_elasticsearch_dsl_drf.pagination import (
    QueryFriendlyPageNumberPagination
)
from .default import BookDocumentViewSet

__all__ = (
    'QueryFriendlyPaginationBookDocumentViewSet',
)


class QueryFriendlyPaginationBookDocumentViewSet(BookDocumentViewSet):

    pagination_class = QueryFriendlyPageNumberPagination
