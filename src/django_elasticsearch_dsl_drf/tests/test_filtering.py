from __future__ import absolute_import

import unittest
import uuid

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

__title__ = 'django_elasticsearch_dsl_drf.tests.test_filtering'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2016-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestFiltering',
)


@pytest.mark.django_db
class TestFiltering(BaseRestFrameworkTestCase):
    """Test filtering."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up."""
        cls.published_count = 10
        cls.published = factories.BookFactory.create_batch(
            cls.published_count,
            **{
                'state': constants.BOOK_PUBLISHING_STATUS_PUBLISHED,
            }
        )

        cls.in_progress_count = 10
        cls.in_progress = factories.BookFactory.create_batch(
            cls.in_progress_count,
            **{
                'state': constants.BOOK_PUBLISHING_STATUS_IN_PROGRESS,
            }
        )

        cls.prefix_count = 2
        cls.prefix = 'DelusionalInsanity'
        cls.prefixed = factories.BookFactory.create_batch(
            cls.prefix_count,
            **{

                'title': '{} {}'.format(cls.prefix, uuid.uuid4()),
                'state': constants.BOOK_PUBLISHING_STATUS_REJECTED
            }
        )

        cls.all_count = (
            cls.published_count +
            cls.in_progress_count +
            cls.prefix_count
        )

        cls.base_url = reverse('bookdocument-list', kwargs={})
        call_command('search_index', '--rebuild', '-f')

    def _field_filter_term(self, field_name, filter_value):
        """Field filter term.

        Example:

            http://localhost:8000/api/articles/?tags=children
        """
        self.authenticate()

        url = self.base_url[:]
        data = {}

        # Should contain 22 results
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), self.all_count)

        # Should contain only 10 results
        filtered_response = self.client.get(
            url + '?{}={}'.format(field_name, filter_value),
            data
        )
        self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(filtered_response.data['results']),
            self.published_count
        )

    def test_field_filter_term(self):
        """Field filter term."""
        return self._field_filter_term(
            'state',
            constants.BOOK_PUBLISHING_STATUS_PUBLISHED
        )

    def _field_filter_range(self, field_name, lower_id, upper_id, count):
        """Field filter range.

        Example:

            http://localhost:8000/api/users/?age__range=16|67
        """
        url = self.base_url[:]
        data = {}
        response = self.client.get(
            url + '?{}__range={}|{}'.format(field_name, lower_id, upper_id),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data['results']),
            count
        )

    def test_field_filter_range(self):
        """Field filter range."""
        lower_id = self.published[0].id
        upper_id = self.published[-1].id
        return self._field_filter_range(
            'id',
            lower_id,
            upper_id,
            self.published_count
        )

    def _field_filter_prefix(self, field_name, prefix, count):
        """Field filter prefix.

        Example:

            http://localhost:8000/api/articles/?tags__prefix=bio
        """
        url = self.base_url[:]
        data = {}
        response = self.client.get(
            url + '?{}__prefix={}'.format(field_name, prefix),
            data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data['results']),
            count
        )

    def test_filter_prefix(self):
        """Test filter prefix."""
        return self._field_filter_prefix(
            'title',
            self.prefix,
            self.prefix_count
        )


if __name__ == '__main__':
    unittest.main()
