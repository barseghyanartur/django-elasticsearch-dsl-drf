"""
Test geo-spatial filtering backend.
"""

from __future__ import absolute_import

import unittest

from django.core.management import call_command

from nine.versions import DJANGO_GTE_1_10

import pytest

from rest_framework import status

import factories

from .base import BaseRestFrameworkTestCase

if DJANGO_GTE_1_10:
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

__title__ = 'django_elasticsearch_dsl_drf.tests.test_filtering'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestFilteringGeoSpatial',
)


@pytest.mark.django_db
class TestFilteringGeoSpatial(BaseRestFrameworkTestCase):
    """Test filtering geo-spatial."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up."""
        cls.base_publisher_url = reverse('publisherdocument-list', kwargs={})

    @pytest.mark.webtest
    def test_field_filter_geo_distance(self):
        """Field filter geo-distance.

        Example:

            http://localhost:8000
            /api/publisher/?location__geo_distance=1km|48.8549|2.3000
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

        __params = '{}|{}|{}'.format(_geo_distance,
                                     _geo_origin.latitude,
                                     _geo_origin.longitude)

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
    def _test_field_filter_geo_polygon(self, field_name, points, count):
        """Private helper test field filter geo-polygon.

        Example:

            http://localhost:8000/api/articles/
            ?location__geo_polygon=3.51,71.46|-47.63,41.64|62.05,29.22

        :param points:
        :param count:
        :type points:
        :type count:
        :return:
        :rtype:
        """
        self.authenticate()

        __params = '{},{}|{},{}|{},{}'.format(
            3.51,
            71.46,
            -47.63,
            41.64,
            62.05,
            29.22,
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
        call_command('search_index', '--rebuild', '-f')
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
        call_command('search_index', '--rebuild', '-f')
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
        call_command('search_index', '--rebuild', '-f')
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
        call_command('search_index', '--rebuild', '-f')
        return self._test_field_filter_geo_polygon(
            field_name='location_2__geo_polygon',
            points=invalid_points,
            count=0
        )

    @pytest.mark.webtest
    def _test_field_filter_geo_bounding_box(self, points, count):
        """Private helper test field filter geo-bounding-box.

        Example:

            http://localhost:8000/api/articles/
            ?location__geo_bounding_box=44.87,40.07|43.87,41.11

        :param points:
        :param count:
        :type points:
        :type count:
        :return:
        :rtype:
        """
        self.authenticate()

        __params = '{},{}|{},{}'.format(
            44.87,
            40.07,
            43.87,
            41.11,
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
        call_command('search_index', '--rebuild', '-f')
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
        call_command('search_index', '--rebuild', '-f')
        return self._test_field_filter_geo_bounding_box(
            points=invalid_points,
            count=0
        )


if __name__ == '__main__':
    unittest.main()
