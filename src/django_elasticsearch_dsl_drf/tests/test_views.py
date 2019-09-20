"""
Test views.
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

__title__ = 'django_elasticsearch_dsl_drf.tests.test_views'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestViews',
)


@pytest.mark.django_db
class TestViews(BaseRestFrameworkTestCase):
    """Test views."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up class."""
        super(TestViews, cls).setUpClass()

        cls.books = factories.BookWithoutTagsAndOrdersFactory.create_batch(20)
        cls.tags = factories.TagGenreFactory.create_batch(20)

        call_command('search_index', '--rebuild', '-f')

    def test_listing_view(self):
        """Test listing view."""
        url = reverse('bookdocument-list', kwargs={})
        data = {}

        # Should contain 20 results
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 20)

    def test_detail_view(self):
        """Test detail view."""
        __obj = self.books[0]
        url = reverse('bookdocument-detail', kwargs={'id': __obj.pk})
        data = {}

        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for __field in ('id', 'title', 'pages', 'state', 'isbn'):
            self.assertEqual(
                response.data[__field],
                getattr(__obj, __field)
            )

    def test_detail_view_with_custom_lookup(self):
        """Test detail view with a custom lookup field."""
        __obj = self.tags[0]
        url = reverse('tagdocument-detail', kwargs={'title': __obj.title})
        data = {}

        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], __obj.title)


if __name__ == '__main__':
    unittest.main()
