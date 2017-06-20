from __future__ import absolute_import

import unittest

from django.core.management import call_command

from nine.versions import DJANGO_GTE_1_10

import pytest

from rest_framework import status

from books import constants
import factories

from .base import BaseTestCase

if DJANGO_GTE_1_10:
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse


@pytest.mark.django_db
class TestFiltering(BaseTestCase):
    """Test filtering."""

    pytestmark = pytest.mark.django_db

    def setUp(self):
        self.published_count = 10
        self.published = factories.BookWithUniqueTitleFactory.create_batch(
            self.published_count,
            **{
                'state': constants.BOOK_PUBLISHING_STATUS_PUBLISHED,
            }
        )

        self.in_progress_count = 10
        self.in_progress = factories.BookWithUniqueTitleFactory.create_batch(
            self.in_progress_count,
            **{
                'state': constants.BOOK_PUBLISHING_STATUS_IN_PROGRESS,
            }
        )

        self.all_count = self.published_count + self.in_progress_count
        call_command('search_index', '--rebuild', '-f')

    def _filter_by_field(self, field_name, filter_value):
        """Filter by field."""
        self.authenticate()

        url = reverse('bookdocument-list', kwargs={})
        data = {}

        # Should contain 20 results
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

    def test_filter_by_field(self):
        """Filter by field."""
        return self._filter_by_field(
            'state',
            constants.BOOK_PUBLISHING_STATUS_PUBLISHED
        )


if __name__ == '__main__':
    unittest.main()
