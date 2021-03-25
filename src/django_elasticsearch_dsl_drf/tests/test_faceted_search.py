"""
Test faceted search backend.
"""

from __future__ import absolute_import

import unittest

from django.core.management import call_command
from django.urls import reverse

import pytest

from rest_framework import status

from books import constants
import factories

from .base import BaseRestFrameworkTestCase

__title__ = 'django_elasticsearch_dsl_drf.tests.test_faceted_search'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestFacetedSearch',
)


@pytest.mark.django_db
class TestFacetedSearch(BaseRestFrameworkTestCase):
    """Test faceted search."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        super(TestFacetedSearch, cls).setUpClass()
        cls.published_count = 11
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

        cls.sleep()
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

        # Should contain `self.all_count` results
        self.assertEqual(len(no_args_response.data['results']), self.all_count)

        # Should contain 1 facets
        self.assertEqual(len(no_args_response.data['facets']), 1)

        # Make request
        facet_state_response = self.client.get(facet_state_url, data)
        self.assertEqual(facet_state_response.status_code, status.HTTP_200_OK)

        # Should contain `self.all_count` results
        self.assertEqual(
            len(facet_state_response.data['results']), self.all_count
        )

        # Should contain 2 facets
        self.assertEqual(len(facet_state_response.data['facets']), 2)
        # With 2 state values
        self.assertEqual(
            len(facet_state_response.data['facets']
                ['_filter_state']['state']['buckets']),
            2
        )

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
        # self.assertIn(
        #     'buckets',
        #     facet_state_response.data['facets']['_filter_state']['state']
        # )
        self.assertIn(
            {
                "doc_count": self.published_count,
                "key": "published"
            },
            facet_state_response.data['facets']
                                     ['_filter_state']
                                     ['state']
                                     ['buckets']
        )
        self.assertIn(
            {
                "doc_count": self.not_published_count,
                "key": "not_published"
            },
            facet_state_response.data['facets']
            ['_filter_state']
            ['state']
            ['buckets']
        )

        filtered_facet_state_url = url + '?facet=state&state={}'.format(
            constants.BOOK_PUBLISHING_STATUS_PUBLISHED
        )
        # Make request
        facet_state_response = self.client.get(filtered_facet_state_url, data)
        self.assertEqual(facet_state_response.status_code, status.HTTP_200_OK)

        # Should contain `self.all_count` results
        self.assertEqual(
            len(facet_state_response.data['results']), self.published_count
        )

        # Should contain 2 facets
        self.assertEqual(len(facet_state_response.data['facets']), 2)
        # With 1 state values
        self.assertEqual(
            len(facet_state_response.data['facets']
                ['_filter_state']['state']['buckets']),
            1
        )

    def test_list_results_with_facets(self):
        """Test list results with facets."""
        return self._list_results_with_facets()


if __name__ == '__main__':
    unittest.main()
