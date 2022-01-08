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
    'TestFacetedFilteredSearch',
)


@pytest.mark.django_db
class TestFacetedFilteredSearch(BaseRestFrameworkTestCase):
    """Test faceted filtered search."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        super(TestFacetedFilteredSearch, cls).setUpClass()

        # published with a known title
        cls.prefixed = factories.BookFactory.create(
            **{
                'title': 'My first book',
                'state': constants.BOOK_PUBLISHING_STATUS_PUBLISHED,
            }
        )

        cls.published_count = 11
        cls.published = factories.BookFactory.create_batch(
            cls.published_count - 1,
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

    def test_list_results_no_facets(self):
        """List results without facets."""
        self.authenticate()
        url = reverse('bookdocument_faceted_filtered-list')

        # Make request
        no_args_response = self.client.get(url)
        self.assertEqual(no_args_response.status_code, status.HTTP_200_OK)

        # Should contain `self.all_count` results
        self.assertEqual(len(no_args_response.data['results']), self.all_count)

        # Should contain no facets
        print(no_args_response.data['facets'])
        self.assertEqual(no_args_response.data['facets'], {})

    def test_list_results_facet_no_filter(self):
        self.authenticate()
        url = reverse('bookdocument_faceted_filtered-list')

        response = self.client.get(url + '?facet=state')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should contain `self.all_count` results
        self.assertEqual(len(response.data['results']), self.all_count)

        # Should contain 1 facet
        self.assertEqual(len(response.data['facets']), 1)
        self.assertEqual(response.data['facets']['_filter_state']['state']['buckets'], [{
            "doc_count": self.published_count,
            "key": "published"
        }, {
            "doc_count": self.not_published_count,
            "key": "not_published"
        }])

    def test_list_results_facet_and_filter(self):
        self.authenticate()
        url = reverse('bookdocument_faceted_filtered-list')

        response = self.client.get(url + '?facet=state&state={}'.format(constants.BOOK_PUBLISHING_STATUS_PUBLISHED))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should contain all published books
        self.assertEqual(len(response.data['results']), self.published_count)

        # Should contain 1 facet
        self.assertEqual(len(response.data['facets']), 1)
        self.assertEqual(response.data['facets']['_filter_state']['state']['buckets'], [{
            "doc_count": self.published_count,
            "key": "published"
        }, {
            "doc_count": self.not_published_count,
            "key": "not_published"
        }])

    def test_list_results_facet_and_filter_on_non_faceted_field(self):
        self.authenticate()
        url = reverse('bookdocument_faceted_filtered-list')

        response = self.client.get(url + '?facet=state&state={}&title={}'.format(
            constants.BOOK_PUBLISHING_STATUS_PUBLISHED,
            'My first book',
        ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should contain 1 result
        self.assertEqual(len(response.data['results']), 1)

        # Should contain 1 facet which matches only the single book, since that is applied as a pre-filter
        self.assertEqual(len(response.data['facets']), 1)
        self.assertEqual(response.data['facets']['_filter_state']['state']['buckets'], [{
            "doc_count": 1,
            "key": "published"
        }])

    def test_list_results_facet_and_filter_only_on_non_faceted_field(self):
        self.authenticate()
        url = reverse('bookdocument_faceted_filtered-list')

        response = self.client.get(url + '?facet=state&title={}'.format('My first book'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should contain 1 result
        self.assertEqual(len(response.data['results']), 1)

        # Should contain 1 facet which matches only the single book, since that is applied as a pre-filter
        self.assertEqual(len(response.data['facets']), 1)
        self.assertEqual(response.data['facets']['_filter_state']['state']['buckets'], [{
            "doc_count": 1,
            "key": "published"
        }])


if __name__ == '__main__':
    unittest.main()
