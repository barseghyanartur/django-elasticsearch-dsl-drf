"""
Test suggestions backend.
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

__title__ = 'django_elasticsearch_dsl_drf.tests.test_suggesters'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestSuggesters',
)


@pytest.mark.django_db
class TestSuggesters(BaseRestFrameworkTestCase):
    """Test suggesters."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up class."""
        cls.publishers = []
        cls.publishers.append(
            factories.PublisherFactory(
                name='Addison–Wesley',
                city='Brighton & Hove',
                state_province='East Midlands',
                country='Armenia',
            )
        )
        cls.publishers.append(
            factories.PublisherFactory(
                name='Adis International',
                city='Bristol',
                state_province='East of England',
                country='Argentina',
            )
        )
        cls.publishers.append(
            factories.PublisherFactory(
                name='Atlantic Books',
                city='Cardiff',
                state_province='North East',
                country='Belgium',
            )
        )
        cls.publishers.append(
            factories.PublisherFactory(
                name='Atlas Press',
                city='Carlisle',
                state_province='North West',
                country='Belarus',
            )
        )
        cls.publishers.append(
            factories.PublisherFactory(
                name='Book League of America',
                city='Chelmsford',
                state_province='South East',
                country='Burkina Faso',
            )
        )
        cls.publishers.append(
            factories.PublisherFactory(
                name='Book Works',
                city='Chester',
                state_province='South West',
                country='Burundi',
            )
        )
        cls.publishers.append(
            factories.PublisherFactory(
                name='Booktrope',
                city='Chichester',
                state_province='West Midlands',
                country='Netherlands',
            )
        )

        call_command('search_index', '--rebuild', '-f')

    def _test_suggesters(self):
        """Test suggesters."""
        self.authenticate()

        url = reverse('publisherdocument-suggest-list', kwargs={})
        data = {}
        test_data = {
            'name_suggest__completion': {
                'Ad': ['Addison–Wesley', 'Adis International'],
                'Atl': ['Atlantic Books', 'Atlas Press'],
                'Boo': ['Book League of America', 'Book Works', 'Booktrope'],
            },
            'country_suggest__completion': {
                'Arm': ['Armenia'],
                'Ar': ['Armenia', 'Argentina'],
                'Bel': ['Belgium', 'Belarus'],
                'Bur': ['Burkina Faso', 'Burundi'],
                'Net': ['Netherlands'],
                'Fra': [],
            }
        }

        for __suggester_field, __test_cases in test_data.items():

            for __test_case, __expected_results in __test_cases.items():
                # Check if response now is valid
                response = self.client.get(
                    url + '?' + __suggester_field + '=' + __test_case,
                    data
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertIn(__suggester_field, response.data)
                self.assertEqual(
                    len(response.data[__suggester_field][0]['options']),
                    len(__expected_results)
                )
                self.assertEqual(
                    sorted([__o['text']
                            for __o
                            in response.data[__suggester_field][0]['options']]),
                    sorted(__expected_results)
                )

    def test_suggesters(self):
        """Test suggesters."""
        return self._test_suggesters()


if __name__ == '__main__':
    unittest.main()
