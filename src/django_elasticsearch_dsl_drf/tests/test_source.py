"""
Test highlight backend.
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

__title__ = 'django_elasticsearch_dsl_drf.tests.test_source'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestSource',
)


@pytest.mark.django_db
class TestSource(BaseRestFrameworkTestCase):
    """Test source."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        super(TestSource, cls).setUpClass()

        cls.books_count = 10
        cls.books = factories.BookFactory.create_batch(
            cls.books_count,
        )

        cls.special_books_count = 10
        cls.special_books = factories.BookFactory.create_batch(
            cls.books_count,
            title='Twenty Thousand Leagues Under the Sea',
            description="""
            The title refers to the distance traveled while under the sea and
            not to a depth, as twenty thousand leagues is over six times the
            diameter, and nearly twice the circumference of the Earth
            """,
            summary="""
            Margaret Drabble argues that Twenty Thousand Leagues Under the Sea
            anticipated the ecology movement and shaped the French avant-garde
            """,
        )
        cls.all_books_count = cls.special_books_count + cls.books_count

        cls.sleep()
        call_command('search_index', '--rebuild', '-f')

    def _list_results(self):
        """List results."""
        self.authenticate()

        url = reverse('bookdocument_source-list', kwargs={}) + '?search=twenty'

        # Make request
        response = self.client.get(url, {})
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Should contain 10 results
        self.assertEqual(
            len(response.data['results']),
            self.special_books_count
        )

        expected_keys = {'id', 'title'}
        # Should only contain 'id' and 'title'.
        for result in response.data['results']:
            self.assertEqual(
                expected_keys,
                set(result.keys())
            )

    def test_list_results(self):
        """Test list results."""
        return self._list_results()


if __name__ == '__main__':
    unittest.main()
