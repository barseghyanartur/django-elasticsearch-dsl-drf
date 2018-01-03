"""
Test pagination.
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

__title__ = 'django_elasticsearch_dsl_drf.tests.test_pagination'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
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
        cls.publishers = factories.PublisherFactory.create_batch(40)
        cls.books = factories.BookFactory.create_batch(40)

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


if __name__ == '__main__':
    unittest.main()
