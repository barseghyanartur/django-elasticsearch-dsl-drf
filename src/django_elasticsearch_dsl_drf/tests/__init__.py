"""
Tests.
"""
from .test_faceted_search import TestFacetedSearch
from .test_filtering_common import TestFilteringCommon
from .test_filtering_geo_spatial import TestFilteringGeoSpatial
from .test_helpers import TestHelpers
from .test_ordering_common import TestOrdering
from .test_ordering_geo_spatial import TestOrderingGeoSpatial
from .test_pagination import TestPagination
from .test_search import TestSearch
from .test_serializers import TestSerializers
from .test_views import TestViews

__title__ = 'django_elasticsearch_dsl_drf.tests'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestFacetedSearch',
    'TestFilteringCommon',
    'TestFilteringGeoSpatial',
    'TestHelpers',
    'TestOrdering',
    'TestOrderingGeoSpatial',
    'TestPagination',
    'TestSearch',
    'TestSerializers',
    'TestViews',
)
