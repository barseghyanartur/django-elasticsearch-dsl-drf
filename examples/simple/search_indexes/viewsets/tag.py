from django_elasticsearch_dsl_drf.constants import (
    FUNCTIONAL_SUGGESTER_COMPLETION_MATCH,
    FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
    LOOKUP_FILTER_GEO_BOUNDING_BOX,
    LOOKUP_FILTER_GEO_DISTANCE,
    LOOKUP_FILTER_GEO_POLYGON,
    SUGGESTER_COMPLETION,
    SUGGESTER_PHRASE,
    SUGGESTER_TERM,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    DefaultOrderingFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
    FunctionalSuggesterFilterBackend,
    GeoSpatialFilteringFilterBackend,
    GeoSpatialOrderingFilterBackend,
)
from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from ..documents import TagDocument
from ..serializers import TagDocumentSerializer

__all__ = (
    'TagDocumentViewSet',
)


class TagDocumentViewSet(DocumentViewSet):
    """Document viewset for tags."""

    document = TagDocument
    serializer_class = TagDocumentSerializer
    lookup_field = 'title'
    filter_backends = []
    pagination_class = LimitOffsetPagination
