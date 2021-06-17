from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from ..documents import TagDocument, NoKeywordTagDocument
from ..serializers import TagDocumentSerializer, NoKeywordTagDocumentSerializer

__all__ = (
    'TagDocumentViewSet',
    'NoKeywordTagDocumentViewSet'
)


class TagDocumentViewSet(DocumentViewSet):
    """Document viewset for tags."""

    document = TagDocument
    serializer_class = TagDocumentSerializer
    lookup_field = 'title'
    filter_backends = []
    pagination_class = LimitOffsetPagination


class NoKeywordTagDocumentViewSet(DocumentViewSet):
    """Document viewset for tags."""

    document = NoKeywordTagDocument
    serializer_class = NoKeywordTagDocumentSerializer
    lookup_field = 'title'
    document_uid_field = 'title'
    filter_backends = []
    pagination_class = LimitOffsetPagination
