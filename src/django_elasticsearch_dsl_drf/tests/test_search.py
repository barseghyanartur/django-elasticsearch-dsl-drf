"""
Test search backend.
"""

from __future__ import absolute_import

import unittest

from django.core.management import call_command

from nine.versions import DJANGO_GTE_1_10

import pytest

from rest_framework import status

from books import constants
import factories
from search_indexes.viewsets import BookDocumentViewSet
from ..filter_backends import SearchFilterBackend

from .base import (
    BaseRestFrameworkTestCase,
    CORE_API_AND_CORE_SCHEMA_ARE_INSTALLED,
    CORE_API_AND_CORE_SCHEMA_MISSING_MSG,
)

if DJANGO_GTE_1_10:
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

__title__ = 'django_elasticsearch_dsl_drf.tests.test_search'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
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
        # Book factories with unique title
        cls.special_count = 10
        cls.special = factories.BookWithUniqueTitleFactory.create_batch(
            cls.special_count,
            **{
                'summary': 'Delusional Insanity, fine art photography',
                'state': constants.BOOK_PUBLISHING_STATUS_PUBLISHED,
            }
        )

        # Lorem ipsum book factories
        cls.lorem_count = 10
        cls.lorem = factories.BookWithUniqueTitleFactory.create_batch(
            cls.lorem_count
        )

        # Book factories with title, description and summary that actually
        # make sense
        cls.non_lorem_count = 9
        cls.non_lorem = [
            factories.BookChapter20Factory(),
            factories.BookChapter21Factory(),
            factories.BookChapter22Factory(),
            factories.BookChapter60Factory(),
            factories.BookChapter61Factory(),
            factories.BookChapter62Factory(),
            factories.BookChapter110Factory(),
            factories.BookChapter111Factory(),
            factories.BookChapter112Factory(),
        ]

        cls.all_count = (
            cls.special_count + cls.lorem_count + cls.non_lorem_count
        )

        cls.cities_count = 20
        cls.cities = factories.CityFactory.create_batch(
            cls.cities_count)
        cls.switzerland = factories.CountryFactory.create(name='Switzerland')
        cls.switz_cities_count = 10
        cls.switz_cities = factories.CityFactory.create_batch(
            cls.switz_cities_count,
            country=cls.switzerland)
        cls.all_cities_count = cls.cities_count + cls.switz_cities_count

        call_command('search_index', '--rebuild', '-f')

        # Testing coreapi and coreschema
        cls.backend = SearchFilterBackend()
        cls.view = BookDocumentViewSet()

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

    def _search_boost(self, search_term, ordering):
        """Search boost.

        In our book view, we have the following defined:

        >>> search_fields = {
        >>>     'title': {'boost': 4},
        >>>     'description': {'boost': 2},
        >>>     'summary': None,
        >>> }

        That means that `title` is more important than `description` and
        `description` is more important than `summary`.
        Results with search term in `title`, `summary` and
        `description` shall be ranked better than results with search term
        in `summary` and `description`. In their turn, results with search term
        in `summary` and `description` shall be ranked better than results
        with search term in `description` only.

        :param search_term:
        :param ordering:
        :return:
        """
        self.authenticate()

        url = reverse('bookdocument_ordered_by_score-list', kwargs={})
        data = {}

        filtered_response = self.client.get(
            url + '?search={}'.format(search_term),
            data
        )
        self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)
        self.assertIn('results', filtered_response.data)
        for counter in len(ordering):
            result_item = filtered_response.data['results'][counter]
            self.assertEqual(result_item.id, ordering[counter])

    def search_boost(self):
        """Search boost.

        :return:
        """
        # Search for "The Pool of Tears"
        self._search_boost(
            search_term="The Pool of Tears",
            ordering=[
                self.non_lorem[0].pk,
                self.non_lorem[1].pk,
                self.non_lorem[2].pk,
            ]
        )

        # Search for "Pig and Pepper"
        self._search_boost(
            search_term="Pig and Pepper",
            ordering=[
                self.non_lorem[3].pk,
                self.non_lorem[4].pk,
                self.non_lorem[5].pk,
            ]
        )

        # Search for "Who Stole the Tarts"
        self._search_boost(
            search_term="Who Stole the Tarts",
            ordering=[
                self.non_lorem[6].pk,
                self.non_lorem[7].pk,
                self.non_lorem[8].pk,
            ]
        )

    def _search_by_nested_field(self, search_term):
        """Search by field."""
        self.authenticate()

        url = reverse('citydocument-list', kwargs={})
        data = {}

        # Should contain 20 results
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), self.all_cities_count)

        # Should contain only 10 results
        filtered_response = self.client.get(
            url + '?search={}'.format(search_term),
            data
        )
        self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(filtered_response.data['results']),
            self.switz_cities_count
        )

    def test_search_by_field(self):
        """Search by field."""
        return self._search_by_field(
            'summary',
            'photography',
        )

    def test_search_by_nested_field(self):
        """Search by field."""
        return self._search_by_nested_field(
            'Switzerland',
        )

    @unittest.skipIf(not CORE_API_AND_CORE_SCHEMA_ARE_INSTALLED,
                     CORE_API_AND_CORE_SCHEMA_MISSING_MSG)
    def test_schema_fields_with_filter_fields_list(self):
        """Test schema field generator"""
        fields = self.backend.get_schema_fields(self.view)
        fields = [f.name for f in fields]
        self.assertEqual(fields, ['search'])

    @unittest.skipIf(not CORE_API_AND_CORE_SCHEMA_ARE_INSTALLED,
                     CORE_API_AND_CORE_SCHEMA_MISSING_MSG)
    def test_schema_field_not_required(self):
        """Test schema fields always not required"""
        fields = self.backend.get_schema_fields(self.view)
        fields = [f.required for f in fields]
        for field in fields:
            self.assertFalse(field)


if __name__ == '__main__':
    unittest.main()
