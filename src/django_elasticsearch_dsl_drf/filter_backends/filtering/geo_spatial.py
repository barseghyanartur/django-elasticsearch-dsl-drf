"""
Geo spatial filtering backend.

Elasticsearch supports two types of geo data:

- geo_point fields which support lat/lon pairs
- geo_shape fields, which support points, lines, circles, polygons,
  multi-polygons etc.

The queries in this group are:

- geo_shape query: Find document with geo-shapes which either intersect,
  are contained by, or do not intersect with the specified geo-shape.
- geo_bounding_box query: Finds documents with geo-points that fall into
  the specified rectangle.
+ geo_distance query: Finds document with geo-points within the specified
  distance of a central point.
- geo_distance_range query: Like the geo_distance query, but the range
  starts at a specified distance from the central point. Note, that this
  one is deprecated and this isn't implemented.
+ geo_polygon query: Find documents with geo-points within the specified
  polygon.
"""

from elasticsearch_dsl.query import Q
from rest_framework.filters import BaseFilterBackend

from six import string_types

from ...constants import (
    ALL_GEO_SPATIAL_LOOKUP_FILTERS_AND_QUERIES,
    LOOKUP_FILTER_GEO_DISTANCE,
    LOOKUP_FILTER_GEO_POLYGON,
    LOOKUP_FILTER_GEO_BOUNDING_BOX,
    SEPARATOR_LOOKUP_COMPLEX_VALUE,
    SEPARATOR_LOOKUP_COMPLEX_MULTIPLE_VALUE,
)
from ..mixins import FilterBackendMixin

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.filtering.common'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('GeoSpatialFilteringFilterBackend',)


class GeoSpatialFilteringFilterBackend(BaseFilterBackend, FilterBackendMixin):
    """Geo-spatial filtering filter backend for Elasticsearch.

    Example:

        >>> from django_elasticsearch_dsl_drf.constants import (
        >>>     LOOKUP_FILTER_GEO_DISTANCE,
        >>> )
        >>> from django_elasticsearch_dsl_drf.filter_backends import (
        >>>     GeoSpatialFilteringFilterBackend
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
        >>>     filter_backends = [GeoSpatialFilteringFilterBackend,]
        >>>     geo_spatial_filter_fields = {
        >>>         'loc': 'location',
        >>>         'location': {
        >>>             'field': 'location',
        >>>             'lookups': [
        >>>                 LOOKUP_FILTER_GEO_DISTANCE,
        >>>             ],
        >>>         }
        >>> }
    """

    @classmethod
    def prepare_filter_fields(cls, view):
        """Prepare filter fields.

        :param view:
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Filtering options.
        :rtype: dict
        """
        filter_fields = view.geo_spatial_filter_fields

        for field, options in filter_fields.items():
            if options is None or isinstance(options, string_types):
                filter_fields[field] = {
                    'field': options or field
                }
            elif 'field' not in filter_fields[field]:
                filter_fields[field]['field'] = field

            if 'lookups' not in filter_fields[field]:
                filter_fields[field]['lookups'] = tuple(
                    ALL_GEO_SPATIAL_LOOKUP_FILTERS_AND_QUERIES
                )

        return filter_fields

    @classmethod
    def get_geo_distance_params(cls, value, field):
        """Get params for `geo_distance` query.

        Example:

            /api/articles/?location__geo_distance=2km|43.53|-12.23

        :param value:
        :param field:
        :type value: str
        :type field:
        :return: Params to be used in `geo_distance` query.
        :rtype: dict
        """
        __values = cls.split_lookup_value(value, maxsplit=3)
        __len_values = len(__values)

        if __len_values < 3:
            return {}

        params = {
            'distance': __values[0],
            field: {
                'lat': __values[1],
                'lon': __values[2],
            }
        }

        if __len_values == 4:
            params['distance_type'] = __values[3]
        else:
            params['distance_type'] = 'sloppy_arc'

        return params

    @classmethod
    def get_geo_polygon_params(cls, value, field):
        """Get params for `geo_polygon` query.

        Example:

            /api/articles/?location__geo_polygon=40,-70|30,-80|20,-90

        Example:

            /api/articles/?location__geo_polygon=40,-70|30,-80|20,-90
                |_name:myname|validation_method:IGNORE_MALFORMED

        Elasticsearch:

            {
                "query": {
                    "bool" : {
                        "must" : {
                            "match_all" : {}
                        },
                        "filter" : {
                            "geo_polygon" : {
                                "person.location" : {
                                    "points" : [
                                        {"lat" : 40, "lon" : -70},
                                        {"lat" : 30, "lon" : -80},
                                        {"lat" : 20, "lon" : -90}
                                    ]
                                }
                            }
                        }
                    }
                }
            }

        :param value:
        :param field:
        :type value: str
        :type field:
        :return: Params to be used in `geo_distance` query.
        :rtype: dict
        """
        __values = cls.split_lookup_value(value)
        __len_values = len(__values)

        if not __len_values:
            return {}

        __points = []
        __options = {}

        for __value in __values:
            if SEPARATOR_LOOKUP_COMPLEX_MULTIPLE_VALUE in __value:
                __lat_lon = __value.split(
                    SEPARATOR_LOOKUP_COMPLEX_MULTIPLE_VALUE
                )
                if len(__lat_lon) >= 2:
                    __points.append(
                        {
                            'lat': float(__lat_lon[0]),
                            'lon': float(__lat_lon[1]),
                        }
                    )

            elif SEPARATOR_LOOKUP_COMPLEX_VALUE in __value:
                __opt_name_val = __value.split(
                    SEPARATOR_LOOKUP_COMPLEX_VALUE
                )
                if len(__opt_name_val) >= 2:
                    if __opt_name_val[0] in ('_name', 'validation_method'):
                        __options.update(
                            {
                                __opt_name_val[0]: __opt_name_val[1]
                            }
                        )

        if __points:
            params = {
                field: {
                    'points': __points
                }
            }
            params.update(__options)

            return params
        return {}

    @classmethod
    def get_geo_bounding_box_params(cls, value, field):
        """Get params for `geo_bounding_box` query.

        Example:

            /api/articles/?location__geo_bounding_box=40.73,-74.1|40.01,-71.12

        Example:

            /api/articles/?location__geo_polygon=40.73,-74.1|40.01,-71.12
                |_name:myname|validation_method:IGNORE_MALFORMED|type:indexed

        Elasticsearch:

            {
                "query": {
                    "bool" : {
                        "must" : {
                            "match_all" : {}
                        },
                        "filter" : {
                            "geo_bounding_box" : {
                                "person.location" : {
                                    "top_left" : {
                                        "lat" : 40.73,
                                        "lon" : -74.1
                                    },
                                    "bottom_right" : {
                                        "lat" : 40.01,
                                        "lon" : -71.12
                                    }
                                }
                            }
                        }
                    }
                }
            }

        :param value:
        :param field:
        :type value: str
        :type field:
        :return: Params to be used in `geo_bounding_box` query.
        :rtype: dict
        """
        __values = cls.split_lookup_value(value)
        __len_values = len(__values)

        if not __len_values:
            return {}

        __top_left_points = {}
        __bottom_right_points = {}
        __options = {}

        # Top left
        __lat_lon = __values[0].split(
            SEPARATOR_LOOKUP_COMPLEX_MULTIPLE_VALUE
        )
        if len(__lat_lon) >= 2:
            __top_left_points.update({
                'lat': float(__lat_lon[0]),
                'lon': float(__lat_lon[1]),
            })

        # Bottom right
        __lat_lon = __values[1].split(
            SEPARATOR_LOOKUP_COMPLEX_MULTIPLE_VALUE
        )
        if len(__lat_lon) >= 2:
            __bottom_right_points.update({
                'lat': float(__lat_lon[0]),
                'lon': float(__lat_lon[1]),
            })

        # Options
        for __value in __values[2:]:
            if SEPARATOR_LOOKUP_COMPLEX_VALUE in __value:
                __opt_name_val = __value.split(
                    SEPARATOR_LOOKUP_COMPLEX_VALUE
                )
                if len(__opt_name_val) >= 2:
                    if __opt_name_val[0] in ('_name',
                                             'validation_method',
                                             'type'):
                        __options.update(
                            {
                                __opt_name_val[0]: __opt_name_val[1]
                            }
                        )

        if not __top_left_points or not __bottom_right_points:
            return {}

        params = {
            field: {
                'top_left': __top_left_points,
                'bottom_right': __bottom_right_points,
            }
        }
        params.update(__options)

        return params

    @classmethod
    def apply_query_geo_distance(cls, queryset, options, value):
        """Apply `geo_distance` query.

        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        return queryset.query(
            Q(
                'geo_distance',
                **cls.get_geo_distance_params(value, options['field'])
            )
        )

    @classmethod
    def apply_query_geo_polygon(cls, queryset, options, value):
        """Apply `geo_polygon` query.

        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        return queryset.query(
            Q(
                'geo_polygon',
                **cls.get_geo_polygon_params(value, options['field'])
            )
        )

    @classmethod
    def apply_query_geo_bounding_box(cls, queryset, options, value):
        """Apply `geo_bounding_box` query.

        :param queryset: Original queryset.
        :param options: Filter options.
        :param value: value to filter on.
        :type queryset: elasticsearch_dsl.search.Search
        :type options: dict
        :type value: str
        :return: Modified queryset.
        :rtype: elasticsearch_dsl.search.Search
        """
        return queryset.query(
            Q(
                'geo_bounding_box',
                **cls.get_geo_bounding_box_params(value, options['field'])
            )
        )

    def get_filter_query_params(self, request, view):
        """Get query params to be filtered on.

        :param request: Django REST framework request.
        :param view: View.
        :type request: rest_framework.request.Request
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Request query params to filter on.
        :rtype: dict
        """
        query_params = request.query_params.copy()

        filter_query_params = {}
        filter_fields = self.prepare_filter_fields(view)
        for query_param in query_params:
            query_param_list = self.split_lookup_filter(
                query_param,
                maxsplit=1
            )
            field_name = query_param_list[0]

            if field_name in filter_fields:
                lookup_param = None
                if len(query_param_list) > 1:
                    lookup_param = query_param_list[1]

                valid_lookups = filter_fields[field_name]['lookups']

                if lookup_param is None or lookup_param in valid_lookups:
                    values = [
                        __value.strip()
                        for __value
                        in query_params.getlist(query_param)
                        if __value.strip() != ''
                    ]

                    if values:
                        filter_query_params[query_param] = {
                            'lookup': lookup_param,
                            'values': values,
                            'field': filter_fields[field_name].get(
                                'field',
                                field_name
                            ),
                            'type': view.mapping
                        }
        return filter_query_params

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
        filter_query_params = self.get_filter_query_params(request, view)
        for options in filter_query_params.values():

            # For all other cases, when we don't have multiple values,
            # we follow the normal flow.
            for value in options['values']:

                # `geo_distance` query lookup
                if options['lookup'] == LOOKUP_FILTER_GEO_DISTANCE:
                    queryset = self.apply_query_geo_distance(
                        queryset,
                        options,
                        value
                    )

                # `geo_polygon` query lookup
                elif options['lookup'] == LOOKUP_FILTER_GEO_POLYGON:
                    queryset = self.apply_query_geo_polygon(
                        queryset,
                        options,
                        value
                    )

                # `geo_bounding_box` query lookup
                elif options['lookup'] == LOOKUP_FILTER_GEO_BOUNDING_BOX:
                    queryset = self.apply_query_geo_bounding_box(
                        queryset,
                        options,
                        value
                    )

        return queryset
