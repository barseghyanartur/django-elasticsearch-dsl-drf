"""
Test faceted search backend.
"""

from __future__ import absolute_import

import unittest

from django.core.management import call_command

from nine.versions import DJANGO_GTE_1_10

import pytest

from rest_framework import status

from books import constants
import factories

from .base import BaseRestFrameworkTestCase

if DJANGO_GTE_1_10:
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

__title__ = 'django_elasticsearch_dsl_drf.tests.test_faceted_search'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestFacetedSearch',
)


@pytest.mark.django_db
class TestFacetedSearch(BaseRestFrameworkTestCase):
    """Test faceted search."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUp(cls):
        cls.published_count = 10
        cls.published = factories.BookFactory.create_batch(
            cls.published_count,
            **{
                'state': constants.BOOK_PUBLISHING_STATUS_PUBLISHED,
            }
        )

        cls.not_published_count = 10
        cls.not_published = factories.BookFactory.create_batch(
            cls.not_published_count,
            **{
                'state': constants.BOOK_PUBLISHING_STATUS_NOT_PUBLISHED,
            }
        )

        cls.all_count = cls.published_count + cls.not_published_count
        call_command('search_index', '--rebuild', '-f')

    def _list_results_with_facets(self):
        """List results with facets."""
        self.authenticate()

        url = reverse('bookdocument-list', kwargs={})
        facet_state_url = url + '?facet=state'
        data = {}

        # Make request
        no_args_response = self.client.get(url, data)
        self.assertEqual(no_args_response.status_code, status.HTTP_200_OK)

        # Should contain 20 results
        self.assertEqual(len(no_args_response.data['results']), self.all_count)

        # Should contain 1 facets
        self.assertEqual(len(no_args_response.data['facets']), 1)

        # Make request
        facet_state_response = self.client.get(facet_state_url, data)
        self.assertEqual(facet_state_response.status_code, status.HTTP_200_OK)

        # Should contain 20 results
        self.assertEqual(
            len(facet_state_response.data['results']), self.all_count
        )

        # Should contain 2 facets
        self.assertEqual(len(facet_state_response.data['facets']), 2)

        self.assertIn('_filter_publisher', facet_state_response.data['facets'])
        self.assertIn(
            'publisher',
            facet_state_response.data['facets']['_filter_publisher']
        )

        self.assertIn('_filter_state', facet_state_response.data['facets'])
        self.assertIn(
            'state',
            facet_state_response.data['facets']['_filter_state']
        )
        self.assertIn(
            'buckets',
            facet_state_response.data['facets']['_filter_state']['state']
        )
        self.assertIn(
            'buckets',
            facet_state_response.data['facets']['_filter_state']['state']
        )
        self.assertIn(
            {
                "doc_count": 10,
                "key": "published"
            },
            facet_state_response.data['facets']
                                     ['_filter_state']
                                     ['state']
                                     ['buckets']
        )
        self.assertIn(
            {
                "doc_count": 10,
                "key": "not_published"
            },
            facet_state_response.data['facets']
            ['_filter_state']
            ['state']
            ['buckets']
        )

    def test_list_results_with_facets(self):
        """Test list results with facets."""
        return self._list_results_with_facets()


if __name__ == '__main__':
    unittest.main()
