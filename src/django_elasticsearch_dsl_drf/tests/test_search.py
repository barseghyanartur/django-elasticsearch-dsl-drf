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

__title__ = 'django_elasticsearch_dsl_drf.tests.test_search'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2016-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestSearch',
)


@pytest.mark.django_db
class TestSearch(BaseRestFrameworkTestCase):
    """Test search."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUp(cls):
        cls.special_count = 10
        cls.special = factories.BookWithUniqueTitleFactory.create_batch(
            cls.special_count,
            **{
                'summary': 'Delusional Insanity, fine art photography',
                'state': constants.BOOK_PUBLISHING_STATUS_PUBLISHED,
            }
        )

        cls.lorem_count = 10
        cls.lorem = factories.BookWithUniqueTitleFactory.create_batch(
            cls.lorem_count
        )

        cls.all_count = cls.special_count + cls.lorem_count
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
