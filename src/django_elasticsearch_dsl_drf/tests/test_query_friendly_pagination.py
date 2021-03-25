"""
Test pagination.
"""

from __future__ import absolute_import

import unittest

from django.core.management import call_command
from django.urls import reverse

from elasticsearch.connection.base import Connection

import pytest

from rest_framework import status

import factories

from .base import BaseRestFrameworkTestCase

__title__ = 'django_elasticsearch_dsl_drf.tests.test_query_friendly_pagination'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestQueryFriendlyPagination',
)

old_log_request_success = Connection.log_request_success
es_call_count = 0


def patched_log_request_success(self, *args, **kwargs):
    global es_call_count
    es_call_count += 1
    old_log_request_success(self, *args, **kwargs)


Connection.log_request_success = patched_log_request_success


@pytest.mark.django_db
class TestQueryFriendlyPagination(BaseRestFrameworkTestCase):
    """Test pagination."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up class."""
        super(TestQueryFriendlyPagination, cls).setUpClass()
        cls.publishers = factories.PublisherFactory.create_batch(43)
        cls.books = factories.BookFactory.create_batch(43)

        cls.sleep()
        call_command('search_index', '--rebuild', '-f')

    def _test_pagination(self):
        """Test pagination."""
        invalid_page_url = self.books_url + '?page=3&page_size=30'

        invalid_response = self.client.get(invalid_page_url, self.data)
        self.assertEqual(
            invalid_response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def _test_pagination_orphans(self):
        """Test pagination returning orphaned nodes"""
        valid_page_url = self.books_url + '?page=1&page_size=40&orphans=3'

        # Check if response now is valid
        valid_response = self.client.get(valid_page_url, self.data)
        self.assertEqual(valid_response.status_code, status.HTTP_200_OK)

        # Check totals
        self.assertEqual(len(valid_response.data['results']), 43)

    def _test_pagination_orphans_over(self):
        """Test pagination when orphaned nodes fall into next page"""
        valid_page_url = self.books_url + '?page=1&page_size=40&orphans=2'

        # Check if response now is valid
        valid_response = self.client.get(valid_page_url, self.data)
        self.assertEqual(valid_response.status_code, status.HTTP_200_OK)

        # Check totals
        self.assertEqual(len(valid_response.data['results']), 40)

        valid_page_url = self.books_url + '?page=2&page_size=40&orphans=2'

        valid_response = self.client.get(valid_page_url, self.data)
        self.assertEqual(valid_response.status_code, status.HTTP_200_OK)

        # Check totals
        self.assertEqual(len(valid_response.data['results']), 3)

    def _test_pagination_offset(self):
        """Test pagination defined by offset and limit"""
        valid_page_url = self.publishers_url + '?limit=5&offset=8'
        valid_response = self.client.get(valid_page_url, self.data)
        self.assertEqual(valid_response.status_code, status.HTTP_200_OK)

        # Check totals
        self.assertEqual(len(valid_response.data['results']), 5)

    def test_pagination(self):
        """Test pagination."""
        self.authenticate()
        self.publishers_url = reverse('publisherdocument-list', kwargs={})
        self.books_url = reverse(
            'bookdocument_query_friendly_pagination-list', kwargs={}
        )
        self.data = {}

        last_es_call_count = es_call_count
        self._test_pagination()
        # Ensure number of ES calls is only 1
        self.assertEqual(es_call_count - last_es_call_count, 1)

        last_es_call_count = es_call_count
        self._test_pagination_orphans()
        # Only in case of orphaned nodes, we need 1 more fallback ES call
        self.assertEqual(es_call_count - last_es_call_count, 2)

        last_es_call_count = es_call_count
        self._test_pagination_orphans_over()
        # Here are two requests
        self.assertEqual(es_call_count - last_es_call_count, 2)

        last_es_call_count = es_call_count
        self._test_pagination_offset()
        self.assertEqual(es_call_count - last_es_call_count, 1)


if __name__ == '__main__':
    unittest.main()
