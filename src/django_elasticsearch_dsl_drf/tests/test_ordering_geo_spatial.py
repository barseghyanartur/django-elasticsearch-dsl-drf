"""
Test geo-spatial ordering filter backend.
"""

from __future__ import absolute_import

import unittest

from django.core.management import call_command

from nine.versions import DJANGO_GTE_1_10

import pytest

from rest_framework import status

import factories

from ..constants import (
    GEO_DISTANCE_ORDERING_PARAM,
    SEPARATOR_LOOKUP_COMPLEX_VALUE,
)
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
    'TestOrderingGeoSpatial',
)


@pytest.mark.django_db
class TestOrderingGeoSpatial(BaseRestFrameworkTestCase):
    """Test ordering geo-spatial."""

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
        cls.unit = 'km'
        cls.algo = 'plane'
        cls.geo_in = []
        for index in range(cls.geo_in_count):
            __publisher = factories.PublisherFactory.create(
                **{
                    'latitude': 48.8570 + index,
                    'longitude': 2.3005,
                }
            )
            cls.geo_in.append(__publisher)

        cls.base_publisher_url = reverse('publisherdocument-list', kwargs={})
        call_command('search_index', '--rebuild', '-f')

    @pytest.mark.webtest
    def test_field_filter_geo_distance(self):
        """Field filter geo_distance.

        Example:

            http://localhost:8000
            /api/publisher/?ordering=location;48.85;2.30;km;plane
        """
        self.authenticate()

        __params = 'location{sep}{lat}{sep}{lon}{sep}{unit}{sep}{algo}'.format(
            lat=self.geo_origin.latitude,
            lon=self.geo_origin.longitude,
            unit=self.unit,
            algo=self.algo,
            sep=SEPARATOR_LOOKUP_COMPLEX_VALUE
        )

        url = self.base_publisher_url[:] + '?{}={}'.format(
            GEO_DISTANCE_ORDERING_PARAM,
            __params
        )

        data = {}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should contain only 6 results
        self.assertEqual(len(response.data['results']), self.geo_in_count + 1)
        item_count = len(response.data['results'])

        for counter, item in enumerate(response.data['results']):
            if (counter > 1) and (counter < item_count + 1):
                self.assertLess(
                    response.data['results'][counter-1]['location']['lat'],
                    response.data['results'][counter]['location']['lat']
                )


if __name__ == '__main__':
    unittest.main()
