"""
Test geo-spatial filtering backend.
"""

from __future__ import absolute_import

from time import sleep
import unittest

from django.core.management import call_command

from elasticsearch.connection.base import TransportError

from nine.versions import DJANGO_GTE_1_10

import pytest

from rest_framework import status

import factories

from ..constants import SEPARATOR_LOOKUP_COMPLEX_VALUE
from .base import BaseRestFrameworkTestCase

if DJANGO_GTE_1_10:
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

__title__ = 'django_elasticsearch_dsl_drf.tests.test_filtering_geo_spatial'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestFilteringGeoSpatial',
)

WAIT_FOR_INDEX = 2


@pytest.mark.django_db
class TestFilteringGeoSpatial(BaseRestFrameworkTestCase):
    """Test filtering geo-spatial."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up."""
        super(TestFilteringGeoSpatial, cls).setUpClass()
        cls.base_publisher_url = reverse('publisherdocument-list', kwargs={})

    def _test_field_filter_geo_distance(self, distance_type=None):
        """Field filter geo-distance.

        Example (distance_type == None):

            http://localhost:8000
            /api/publisher/?location__geo_distance=1km__48.8549__2.3000

        Example (distance_type == 'arc'):

            http://localhost:8000
            /api/publisher/?location__geo_distance=1km__48.8549__2.3000__arc
        """
        self.authenticate()

        _geo_origin = factories.PublisherFactory.create(
            **{
                'latitude': 48.8549,
                'longitude': 2.3000,
            }
        )

        _geo_in_count = 5
        _geo_distance = '1km'
        _geo_in = factories.PublisherFactory.create_batch(
            _geo_in_count,
            **{
                'latitude': 48.8570,
                'longitude': 2.3005,
            }
        )

        call_command('search_index', '--rebuild', '-f')
        sleep(WAIT_FOR_INDEX)

        __params = '{distance}{separator}{lat}{separator}{lon}{d_type}'.format(
            distance=_geo_distance,
            lat=_geo_origin.latitude,
            lon=_geo_origin.longitude,
            separator=SEPARATOR_LOOKUP_COMPLEX_VALUE,
            d_type='__{}'.format(distance_type) if distance_type else ''
        )

        url = self.base_publisher_url[:] + '?{}={}'.format(
            'location__geo_distance',
            __params
        )

        data = {}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should contain only 6 results
        self.assertEqual(len(response.data['results']), _geo_in_count + 1)

    @pytest.mark.webtest
    def test_field_filter_geo_distance(self):
        """Field filter geo-distance.

        Example:

            http://localhost:8000
            /api/publisher/?location__geo_distance=1km__48.8549__2.3000

        :return:
        """
        return self._test_field_filter_geo_distance()

    @pytest.mark.webtest
    def test_field_filter_geo_distance_distance_type_arc(self):
        """Field filter geo-distance.

        Example:

            http://localhost:8000
            /api/publisher/?location__geo_distance=1km__48.8549__2.3000__arc

        :return:
        """
        return self._test_field_filter_geo_distance(distance_type='arc')

    @pytest.mark.webtest
    def test_field_filter_geo_distance_not_enough_args_fail(self):
        """Field filter geo-distance. Fail test on not enough args.

        Example:

            http://localhost:8000
            /api/publisher/?location__geo_distance=1km__48.8549

        :return:
        """
        self.authenticate()
        _geo_origin = factories.PublisherFactory.create(
            **{
                'latitude': 48.8549,
                'longitude': 2.3000,
            }
        )
        _geo_in_count = 5
        _geo_distance = '1km'
        _geo_in = factories.PublisherFactory.create_batch(
            _geo_in_count,
            **{
                'latitude': 48.8570,
                'longitude': 2.3005,
            }
        )

        call_command('search_index', '--rebuild', '-f')
        sleep(WAIT_FOR_INDEX)

        __params = '{distance}{separator}{lat}'.format(
            distance=_geo_distance,
            lat=_geo_origin.latitude,
            separator=SEPARATOR_LOOKUP_COMPLEX_VALUE,
        )
        url = self.base_publisher_url[:] + '?{}={}'.format(
            'location__geo_distance',
            __params
        )
        data = {}
        with self.assertRaises(TransportError) as context:
            response = self.client.get(url, data)

    @pytest.mark.webtest
    def _test_field_filter_geo_polygon(self, field_name, points, count):
        """Private helper test field filter geo-polygon.

        Example:

            http://localhost:8000/api/articles/
            ?location__geo_polygon=3.51,71.46__-47.63,41.64__62.05,29.22

        :param points:
        :param count:
        :type points:
        :type count:
        :return:
        :rtype:
        """
        self.authenticate()

        __params = '{val1},{val2}{sep}{val3},{val4}{sep}{val5},{val6}'.format(
            val1=3.51,
            val2=71.46,
            val3=-47.63,
            val4=41.64,
            val5=62.05,
            val6=29.22,
            sep=SEPARATOR_LOOKUP_COMPLEX_VALUE
        )

        publishers = []

        url = self.base_publisher_url[:] + '?{}={}'.format(
            field_name,
            __params
        )
        data = {}

        for __lat, __lon in points:
            publishers.append(
                factories.PublisherFactory(
                    latitude=__lat,
                    longitude=__lon,
                )
            )

        call_command('search_index', '--rebuild', '-f')
        sleep(WAIT_FOR_INDEX)

        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), count)

        return publishers

    @pytest.mark.webtest
    def test_field_filter_geo_polygon(self):
        """Test field filter geo-polygon.

        :return:
        """
        valid_points = [
            (-23.37, 47.51),
            (-2.81, 63.15),
            (15.99, 46.31),
            (26.54, 42.42),
        ]

        return self._test_field_filter_geo_polygon(
            field_name='location__geo_polygon',
            points=valid_points,
            count=4
        )

    @pytest.mark.webtest
    def test_field_filter_geo_polygon_fail_test(self):
        """Test field filter geo-polygon (fail test).

        :return:
        """
        invalid_points = [
            (-82.79, 72.34),
            (54.31, 72.34),
            (-6.50, 78.42),
            (-56.42, 82.78),
        ]

        return self._test_field_filter_geo_polygon(
            field_name='location__geo_polygon',
            points=invalid_points,
            count=0
        )

    @pytest.mark.webtest
    def test_field_filter_geo_polygon_string_options(self):
        """Test field filter geo-polygon.

        :return:
        """
        valid_points = [
            (-23.37, 47.51),
            (-2.81, 63.15),
            (15.99, 46.31),
            (26.54, 42.42),
        ]

        return self._test_field_filter_geo_polygon(
            field_name='location_2__geo_polygon',
            points=valid_points,
            count=4
        )

    @pytest.mark.webtest
    def test_field_filter_geo_polygon_string_options_fail_test(self):
        """Test field filter geo-polygon (fail test).

        :return:
        """
        invalid_points = [
            (-82.79, 72.34),
            (54.31, 72.34),
            (-6.50, 78.42),
            (-56.42, 82.78),
        ]

        return self._test_field_filter_geo_polygon(
            field_name='location_2__geo_polygon',
            points=invalid_points,
            count=0
        )

    @pytest.mark.webtest
    def _test_field_filter_geo_bounding_box(self, points, count):
        """Private helper test field filter geo-bounding-box.

        For testing use
        http://bboxfinder.com/#40.070000,43.870000,41.110000,44.870000

        Example:

            http://localhost:8000/api/articles/
            ?location__geo_bounding_box=44.87,40.07__43.87,41.11

        :param points:
        :param count:
        :type points:
        :type count:
        :return:
        :rtype:
        """
        self.authenticate()

        __params = '{val1},{val2}{sep}{val3},{val4}'.format(
            val1=44.87,
            val2=40.07,
            val3=43.87,
            val4=41.11,
            sep=SEPARATOR_LOOKUP_COMPLEX_VALUE
        )

        publishers = []

        url = self.base_publisher_url[:] + '?{}={}'.format(
            'location__geo_bounding_box',
            __params
        )
        data = {}

        for __lat, __lon in points:
            publishers.append(
                factories.PublisherFactory(
                    latitude=__lat,
                    longitude=__lon,
                )
            )

        call_command('search_index', '--rebuild', '-f')
        sleep(WAIT_FOR_INDEX)

        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), count)

        return publishers

    @pytest.mark.webtest
    def test_field_filter_geo_bounding_box(self):
        """Test field filter geo-bounding-box.

        :return:
        """
        valid_points = [
            (44.18, 40.86),
            (44.61, 40.80),
            (44.32, 40.51),
            (44.60, 40.40),
        ]

        return self._test_field_filter_geo_bounding_box(
            points=valid_points,
            count=4
        )

    @pytest.mark.webtest
    def test_field_filter_geo_bounding_box_fail_test(self):
        """Test field filter geo-bounding-box (fail test).

        :return:
        """
        invalid_points = [
            (-82.79, 72.34),
            (54.31, 72.34),
            (-6.50, 78.42),
            (-56.42, 82.78),
            (45.20, 39.93),
            (43.71, 41.29),
        ]

        return self._test_field_filter_geo_bounding_box(
            points=invalid_points,
            count=0
        )


if __name__ == '__main__':
    unittest.main()
