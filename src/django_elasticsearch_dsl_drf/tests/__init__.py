"""
Tests.
"""
from .test_faceted_search import TestFacetedSearch
from .test_filtering_common import TestFilteringCommon
from .test_filtering_geo_spatial import TestFilteringGeoSpatial
from .test_filtering_global_aggregations import TestFilteringGlobalAggregations
from .test_filtering_nested import TestFilteringNested
from .test_filtering_post_filter import TestFilteringPostFilter
from .test_functional_suggesters import TestFunctionalSuggesters
from .test_helpers import TestHelpers
from .test_highlight import TestHighlight
# from .test_more_like_this import TestMoreLikeThis
from .test_ordering_common import TestOrdering
from .test_ordering_geo_spatial import TestOrderingGeoSpatial
from .test_pagination import TestPagination
from .test_pip_helpers import TestPipHelpers
from .test_search import TestSearch
from .test_search_multi_match import TestMultiMatchSearch
from .test_search_simple_query_string import TestSimpleQueryStringSearch
from .test_serializers import TestSerializers
from .test_suggesters import TestSuggesters
from .test_views import TestViews
from .test_wrappers import TestWrappers

__title__ = 'django_elasticsearch_dsl_drf.tests'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestFacetedSearch',
    'TestFilteringCommon',
    'TestFilteringGeoSpatial',
    'TestFilteringGlobalAggregations',
    'TestFilteringNested',
    'TestFilteringPostFilter',
    'TestFunctionalSuggesters',
    'TestHelpers',
    'TestHighlight',
    # 'TestMoreLikeThis',
    'TestMultiMatchSearch',
    'TestSimpleQueryStringSearch',
    'TestOrdering',
    'TestOrderingGeoSpatial',
    'TestPagination',
    'TestPipHelpers',
    'TestSearch',
    'TestSerializers',
    'TestSuggesters',
    'TestViews',
    'TestWrappers',
)
