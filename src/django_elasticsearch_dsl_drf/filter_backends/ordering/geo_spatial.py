"""
Geo-spatial ordering backend.
"""

from rest_framework.filters import BaseFilterBackend


from ..mixins import FilterBackendMixin
from ...constants import (
    GEO_DISTANCE_ORDERING_PARAM,
)

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.ordering.common'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('GeoSpatialOrderingFilterBackend',)


class GeoSpatialOrderingFilterBackend(BaseFilterBackend, FilterBackendMixin):
    """Geo-spatial ordering filter backend for Elasticsearch.

    Example:

        >>> from django_elasticsearch_dsl_drf.filter_backends import (
        >>>     GeoSpatialOrderingFilterBackend
        >>> )
        >>> from django_elasticsearch_dsl_drf.views import BaseDocumentViewSet
        >>>
        >>> # Local article document definition
        >>> from .documents import ArticleDocument
        >>>
        >>> # Local article document serializer
        >>> from .serializers import ArticleDocumentSerializer
        >>>
        >>> class ArticleDocumentView(BaseDocumentViewSet):
        >>>
        >>>     document = ArticleDocument
        >>>     serializer_class = ArticleDocumentSerializer
        >>>     filter_backends = [GeoSpatialOrderingFilterBackend,]
        >>>     geo_spatial_ordering_fields = {
        >>>         'location': {
        >>>             'field': 'location',
        >>>         }
        >>>     }
    """

    ordering_param = GEO_DISTANCE_ORDERING_PARAM

    @classmethod
    def get_geo_distance_params(cls, value, field):
        """Get params for `geo_distance` ordering.

        Example:

            /api/articles/?ordering=-location|45.3214|-34.3421|km|planes

        :param value:
        :param field:
        :type value: str
        :type field:
        :return: Params to be used in `geo_distance` query.
        :rtype: dict
        """
        __values = cls.split_lookup_value(value, maxsplit=3)
        __len_values = len(__values)

        if __len_values < 2:
            return {}

        params = {
            field: {
                'lat': __values[0],
                'lon': __values[1],
            }
        }

        if __len_values > 2:
            params['unit'] = __values[2]
        else:
            params['unit'] = 'm'
        if __len_values > 3:
            params['distance_type'] = __values[3]
        else:
            params['distance_type'] = 'sloppy_arc'

        return params

    def get_ordering_query_params(self, request, view):
        """Get ordering query params.

        :param request: Django REST framework request.
        :param view: View.
        :type request: rest_framework.request.Request
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Ordering params to be used for ordering.
        :rtype: list
        """
        # TODO: Support `mode` argument.
        query_params = request.query_params.copy()
        ordering_query_params = query_params.getlist(self.ordering_param, [])
        __ordering_params = []
        # Remove invalid ordering query params
        for query_param in ordering_query_params:
            __key, __value = FilterBackendMixin.split_lookup_value(
                query_param.lstrip('-'),
                maxsplit=1,
            )
            __direction = 'desc' if query_param.startswith('-') else 'asc'
            if __key in view.geo_spatial_ordering_fields:
                __field_name = view.geo_spatial_ordering_fields[__key] or __key
                __params = self.get_geo_distance_params(__value, __field_name)
                __params['order'] = __direction
                __ordering_params.append(__params)

        return __ordering_params

    def filter_queryset(self, request, queryset, view):
        """Filter the queryset.

        :param request: Django REST framework request.
        :param queryset: Base queryset.
        :param view: View.
        :type request: rest_framework.request.Request
        :type queryset: elasticsearch_dsl.search.Search
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Updated queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        ordering_query_params = self.get_ordering_query_params(request, view)

        if ordering_query_params:
            return queryset.sort(*ordering_query_params)

        return queryset
