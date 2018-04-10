"""
The ``post_filter`` filtering backends.
"""

from .common import PostFilterFilteringFilterBackend
# from .ids import IdsFilterBackend
# from .geo_spatial import GeoSpatialFilteringFilterBackend

__title__ = 'django_elasticsearch_dsl_drf.filter_backends.filtering.' \
            'post_filter'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'PostFilterFilteringFilterBackend',
    # 'GeoSpatialFilteringFilterBackend',
    # 'IdsFilterBackend',
)
