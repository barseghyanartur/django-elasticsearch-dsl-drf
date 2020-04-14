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

__title__ = 'django_elasticsearch_dsl_drf.tests.test_highlight'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestHighlight',
)


@pytest.mark.django_db
class TestHighlight(BaseRestFrameworkTestCase):
    """Test highlight."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        super(TestHighlight, cls).setUpClass()
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

    def _list_results_with_highlights(self):
        """List results with facets."""
        self.authenticate()

        url = reverse('bookdocument-list', kwargs={}) + '?search=twenty'
        all_highlights_url = url + '&highlight=summary&highlight=description'

        # Make request
        no_args_response = self.client.get(url, {})
        self.assertEqual(no_args_response.status_code, status.HTTP_200_OK)

        # Should contain 10 results
        self.assertEqual(
            len(no_args_response.data['results']), self.special_books_count)

        for result in no_args_response.data['results']:
            self.assertEqual(list(result['highlight'].keys()), ['title'])

        # Make request
        all_highlights_response = self.client.get(all_highlights_url, {})
        self.assertEqual(
            all_highlights_response.status_code, status.HTTP_200_OK)

        # Should contain 20 results
        self.assertEqual(
            len(all_highlights_response.data['results']),
            self.special_books_count,
        )
        for result in all_highlights_response.data['results']:
            self.assertEqual(set(['title', 'description', 'summary']),
                             set(result['highlight'].keys()))

    def test_list_results_with_highlights(self):
        """Test list results with facets."""
        return self._list_results_with_highlights()


if __name__ == '__main__':
    unittest.main()
