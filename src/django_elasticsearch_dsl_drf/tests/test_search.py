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
class TestSearch(BaseTestCase):
    """Test search."""

    pytestmark = pytest.mark.django_db

    def setUp(self):
        self.special_count = 10
        self.special = factories.BookWithUniqueTitleFactory.create_batch(
            self.special_count,
            **{
                'summary': 'Delusional Insanity, fine art photography',
                'state': constants.BOOK_PUBLISHING_STATUS_PUBLISHED,
            }
        )

        self.lorem_count = 10
        self.lorem = factories.BookWithUniqueTitleFactory.create_batch(
            self.lorem_count
        )

        self.all_count = self.special_count + self.lorem_count
        call_command('search_index', '--rebuild', '-f')

    def _search_by_field(self, field_name, search_term):
        """Search by field."""
        self.authenticate()

        url = reverse('bookdocument-list', kwargs={})
        data = {}

        # Should contain 20 results
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), self.all_count)

        # Should contain only 10 results
        filtered_response = self.client.get(
            url + '?search={}'.format(search_term),
            data
        )
        self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(filtered_response.data['results']),
            self.special_count
        )

    def test_search_by_field(self):
        """Search by field."""
        return self._search_by_field(
            'summary',
            'photography',
        )


if __name__ == '__main__':
    unittest.main()
