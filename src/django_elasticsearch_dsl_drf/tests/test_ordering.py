from __future__ import absolute_import

import unittest

from django.core.management import call_command
from django.urls import reverse

import pytest

from rest_framework import status

import factories

from .base import BaseTestCase


@pytest.mark.django_db
class TestOrdering(BaseTestCase):
    """Test ordering."""

    pytestmark = pytest.mark.django_db

    def setUp(self):
        self.books = factories.BookWithUniqueTitleFactory.create_batch(20)

        call_command('search_index', '--rebuild', '-f')

    def _order_by_field(self, field_name):
        """Order by field."""
        self.authenticate()

        url = reverse('bookdocument-list', kwargs={})
        data = {}

        # Should contain 20 results
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Order should be descending
        filtered_response = self.client.get(
            url + '?ordering={}'.format(field_name),
            data
        )
        self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)

        item_count = len(filtered_response.data['results'])

        for counter, item in enumerate(filtered_response.data['results']):
            if (counter > 1) and (counter < item_count + 1):
                self.assertGreater(
                    filtered_response.data['results'][counter-1]['id'],
                    filtered_response.data['results'][counter]['id']
                )

    def test_order_by_field(self):
        """Order by field."""
        return self._order_by_field('-id')


if __name__ == '__main__':
    unittest.main()
