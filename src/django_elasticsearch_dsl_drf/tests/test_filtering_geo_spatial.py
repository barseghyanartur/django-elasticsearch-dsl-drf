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
__copyright__ = '2017 Artur Barseghyan'
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
        cls.geo_origin = factories.PublisherFactory.create(
            **{
                'latitude': 48.8549,
                'longitude': 2.3000,
            }
        )

        cls.geo_in_count = 5
        cls.geo_distance = '1km'
        cls.geo_in = factories.PublisherFactory.create_batch(
            cls.geo_in_count,
            **{
                'latitude': 48.8570,
                'longitude': 2.3005,
            }
        )

        cls.base_publisher_url = reverse('publisherdocument-list', kwargs={})
        call_command('search_index', '--rebuild', '-f')

    @pytest.mark.webtest
    def test_field_filter_geo_distance(self):
        """Field filter geo-distance.

        Example:

            http://localhost:8000
            /api/publisher/?location__geo_distance=1km|48.8549|2.3000
        """
        self.authenticate()

        __params = '{}|{}|{}'.format(self.geo_distance,
                                     self.geo_origin.latitude,
                                     self.geo_origin.longitude)

        url = self.base_publisher_url[:] + '?{}={}'.format(
            'location__geo_distance',
            __params
        )

        data = {}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should contain only 6 results
        self.assertEqual(len(response.data['results']), self.geo_in_count + 1)

    @pytest.mark.webtest
    def test_field_filter_geo_polygon(self):
        """Field filter geo-polygon.

        Example:

            http://localhost:8000/api/articles/
            ?location__geo_polygon=3.51,-71.46|-47.63,41.64|62.05,29.22
        """
        self.authenticate()

        __params = '{},{}|{},{}|{},{}'.format(
            3.51,
            -71.46,
            -47.63,
            41.64,
            62.05,
            29.22,
        )

        valid_points = [
            (-23.37, 47.51),
            (-2.81, 63.15),
            (15.99, 46.31),
            (26.54, 42.42),
        ]

        invalid_points = [
            (-82.79, 72.34),
            (54.31, 72.34),
            (-6.50, 78.42),
            # (-56.42, 82.78),
        ]
        valid_publishers = []
        invalid_publishers = []

        for __lat, __lon in valid_points:
            valid_publishers.append(
                factories.PublisherFactory(
                    latitude=__lat,
                    longitude=__lon,
                )
            )

        for __lat, __lon in invalid_points:
            invalid_publishers.append(
                factories.PublisherFactory(
                    latitude=__lat,
                    longitude=__lon,
                )
            )

        url = self.base_publisher_url[:] + '?{}={}'.format(
            'location__geo_polygon',
            __params
        )

        data = {}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should contain only 4 results
        self.assertEqual(len(response.data['results']), 4)


if __name__ == '__main__':
    unittest.main()
