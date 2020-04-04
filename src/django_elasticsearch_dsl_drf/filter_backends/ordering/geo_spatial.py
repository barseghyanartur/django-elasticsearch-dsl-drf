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
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('GeoSpatialOrderingFilterBackend',)


class GeoSpatialOrderingFilterBackend(BaseFilterBackend, FilterBackendMixin):
    """Geo-spatial ordering filter backend for Elasticsearch.

    Example:

        >>> from django_elasticsearch_dsl_drf.filter_backends import (
        >>>     GeoSpatialOrderingFilterBackend
        >>> )
        >>> from django_elasticsearch_dsl_drf.viewsets import (
        >>>     BaseDocumentViewSet,
        >>> )
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

            /api/articles/?ordering=-location__45.3214__-34.3421__km__planes

        :param value:
        :param field:
        :type value: str
        :type field:
        :return: Params to be used in `geo_distance` query.
        :rtype: dict
        """
        __values = cls.split_lookup_complex_value(value, maxsplit=3)
        __len_values = len(__values)

        if __len_values < 2:
            return {}

        params = {
            '_geo_distance': {
                field: {
                    'lat': __values[0],
                    'lon': __values[1],
                }
            }
        }

        if __len_values > 2:
            params['_geo_distance']['unit'] = __values[2]
        else:
            params['_geo_distance']['unit'] = 'm'
        if __len_values > 3:
            params['_geo_distance']['distance_type'] = __values[3]
        else:
            params['_geo_distance']['distance_type'] = 'arc'

        return params

    def get_geo_spatial_field_name(self, request, view, name):
        """Get geo-spatial field name.

        We have to deal with a couple of situations here:

        Example 1:

         >>> geo_spatial_ordering_fields = {
         >>>     'location': None,
         >>> }

        Example 2:

        >>> geo_spatial_ordering_fields = {
        >>>     'location': 'location',
        >>> }

        Example 3:

        >>> geo_spatial_ordering_fields = {
        >>>     'location': {
        >>>         'field': 'location'
        >>>     },
        >>> }

        :param request:
        :param view:
        :param name:
        :return:
        """
        options = view.geo_spatial_ordering_fields[name]
        if options is None:
            return name
        elif isinstance(options, dict):
            if 'field' in options:
                return options['field']
        else:
            return options

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
            try:
                __key, __value = FilterBackendMixin.split_lookup_complex_value(
                    query_param.lstrip('-'),
                    maxsplit=1,
                )
            # Probably using both
            # OrderingFilterBackend/DefaultOrderingFilterBackend
            # and GeoSpatialOrderingFilterBackend
            except ValueError:
                break
            __direction = 'desc' if query_param.startswith('-') else 'asc'
            if __key in view.geo_spatial_ordering_fields:
                __field_name = self.get_geo_spatial_field_name(
                    request,
                    view,
                    __key
                )
                __params = self.get_geo_distance_params(__value, __field_name)
                __params['_geo_distance']['order'] = __direction
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
