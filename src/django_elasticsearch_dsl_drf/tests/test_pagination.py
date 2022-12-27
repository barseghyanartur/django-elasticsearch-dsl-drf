"""
Test pagination.
"""
import pytest

from anysearch import IS_OPENSEARCH
from django.core.management import call_command
from django.urls import reverse

from rest_framework import status

import factories

from .base import BaseRestFrameworkTestCase

__title__ = 'django_elasticsearch_dsl_drf.tests.test_pagination'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2022 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestPagination',
)


@pytest.mark.django_db
class TestPagination(BaseRestFrameworkTestCase):
    """Test pagination."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up class."""
        super(TestPagination, cls).setUpClass()
        cls.publishers = factories.PublisherFactory.create_batch(40)
        cls.books = factories.BookFactory.create_batch(40)

        cls.sleep()
        call_command('search_index', '--rebuild', '-f')

    def _test_pagination(self):
        """Test pagination."""
        self.authenticate()

        publishers_url = reverse('publisherdocument-list', kwargs={})
        books_url = reverse('bookdocument-list', kwargs={})
        data = {}

        invalid_page_url = books_url + '?page=3&page_size=30'

        invalid_response = self.client.get(invalid_page_url, data)
        self.assertEqual(
            invalid_response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        valid_page_url = publishers_url + '?limit=5&offset=8'

        # Check if response now is valid
        valid_response = self.client.get(valid_page_url, data)
        self.assertEqual(valid_response.status_code, status.HTTP_200_OK)

        # Check totals
        self.assertEqual(len(valid_response.data['results']), 5)

    def test_pagination(self):
        """Test pagination."""
        return self._test_pagination()
