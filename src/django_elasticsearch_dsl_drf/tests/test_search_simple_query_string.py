"""
Test multi match search filter backend.
"""

from __future__ import absolute_import

import unittest

from django.core.management import call_command

from nine.versions import DJANGO_GTE_1_10

import pytest

from rest_framework import status

from books import constants
import factories
from search_indexes.viewsets import (
    BookSimpleQueryStringSearchFilterBackendDocumentViewSet
)
from ..filter_backends import SimpleQueryStringSearchFilterBackend
from ..versions import ELASTICSEARCH_GTE_6_0

from .base import (
    BaseRestFrameworkTestCase,
    CORE_API_AND_CORE_SCHEMA_ARE_INSTALLED,
    CORE_API_AND_CORE_SCHEMA_MISSING_MSG,
)

if DJANGO_GTE_1_10:
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

__title__ = 'django_elasticsearch_dsl_drf.tests.test_search_multi_match'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestSimpleQueryStringSearch',
)


@pytest.mark.django_db
class TestSimpleQueryStringSearch(BaseRestFrameworkTestCase):
    """Test simple query string search."""

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
        cls.cities = factories.CityFactory.create_batch(cls.cities_count)

        # Create 10 cities in a given country. The reason that we don't
        # do create_batch here is that sometimes in the same test city name is
        # generated twice and thus our concept of precise number matching
        # fails. Before there's a better approach, this would stay so. The
        # create_batch part (below) will remain commented out, until there's a
        # better solution.
        cls.switzerland = factories.CountryFactory.create(name='Wonderland')
        cls.switz_cities_count = 10
        cls.switz_cities_names = [
            'Zurich',
            'Geneva',
            'Basel',
            'Lausanne',
            'Bern',
            'Winterthur',
            'Lucerne',
            'St. Gallen',
            'Lugano',
            'Biel/Bienne',
        ]
        for switz_city in cls.switz_cities_names:
            cls.switz_cities = factories.CityFactory(
                name=switz_city,
                country=cls.switzerland
            )
        # cls.switz_cities = factories.CityFactory.create_batch(
        #     cls.switz_cities_count,
        #     country=cls.switzerland
        # )
        cls.all_cities_count = cls.cities_count + cls.switz_cities_count

        call_command('search_index', '--rebuild', '-f')

        # Testing coreapi and coreschema
        cls.backend = SimpleQueryStringSearchFilterBackend()
        cls.view = BookSimpleQueryStringSearchFilterBackendDocumentViewSet()

    def _search(self, search_term, num_results, url=None):
        """Search."""
        self.authenticate()

        if url is None:
            url = reverse(
                'bookdocument_simple_query_string_search_backend-list',
                kwargs={}
            )

        data = {}

        # Should contain 20 results
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), self.all_count)

        # Should contain only 10 results
        filtered_response = self.client.get(
            url + '?search_simple_query_string={}'.format(search_term),
            data
        )
        self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(filtered_response.data['results']),
            num_results
        )

    def _search_boost(self, search_term, ordering, url=None):
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

        if url is None:
            url = reverse(
                'bookdocument_simple_query_string_search_backend-list',
                kwargs={}
            )
        data = {}

        filtered_response = self.client.get(
            url + '?search_simple_query_string={}'.format(search_term),
            data
        )
        self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)
        self.assertIn('results', filtered_response.data)
        for counter, item_id in enumerate(ordering):
            result_item = filtered_response.data['results'][counter]
            self.assertEqual(result_item['id'], item_id)

    def test_search_with_quotes(self, url=None):
        """Search with quotes."""
        # Search for: "Pig and Pepper"
        self._search(
            search_term='"Pig and Pepper"',
            num_results=1,
            url=url
        )

        # Search for: "Pool of Tears"
        self._search(
            search_term='"Pool of Tears"',
            num_results=3,
            url=url
        )

        # Search for: "Pool of Tears" -considering
        self._search(
            search_term='"Pool of Tears" -considering',
            num_results=1,
            url=url
        )

        # Search for: "chapter II" +fender. Note, that `%2B` stands for `+`
        # symbol in the URL.
        self._search(
            search_term='"chapter II" %2Bfender',
            num_results=1,
            url=url
        )

        # Search for: "chapter II" +shutting. Note, that `%2B` stands for `+`
        # symbol in the URL.
        self._search(
            search_term='"chapter II" %2Bshutting',
            num_results=1,
            url=url
        )

        # Search for: "chapter II" +(shutting | fender). Note, that `%2B`
        # stands for `+` symbol in the URL.
        self._search(
            search_term='"chapter II" %2B(shutting | fender)',
            num_results=2,
            url=url
        )

    @unittest.skipIf(condition=ELASTICSEARCH_GTE_6_0, reason="")
    def test_search_without_quotes(self, url=None):
        """Test search without quotes. This does not work on Elasticsearch 6.x.

        :param url:
        :return:
        """
        # Search for: Pig and Pepper
        self._search(
            search_term='Pig and Pepper',
            num_results=2,
            url=url
        )

    def test_search_with_quotes_boost(self, url=None):
        """Search boost.

        :return:
        """
        # Search for: "Pig and Pepper"
        self._search_boost(
            search_term='"Pig and Pepper"',
            ordering=[
                self.non_lorem[3].pk,
            ],
            url=url
        )

        # Search for: "Pool of Tears"
        self._search_boost(
            search_term='"Pool of Tears"',
            ordering=[
                self.non_lorem[0].pk,
                self.non_lorem[1].pk,
                self.non_lorem[2].pk,
            ],
            url=url
        )

        # Search for: "Pool of Tears" -considering
        self._search_boost(
            search_term='"Pool of Tears" -considering',
            ordering=[
                self.non_lorem[0].pk,
            ],
            url=url
        )

        # Search for: "chapter II" +fender. Note, that `%2B` stands for `+`
        self._search_boost(
            search_term='"chapter II" %2Bfender',
            ordering=[
                self.non_lorem[2].pk,
            ],
            url=url
        )

        # Search for: "chapter II" +shutting. Note, that `%2B` stands for `+`
        # symbol in the URL.
        self._search_boost(
            search_term='"chapter II" %2Bshutting',
            ordering=[
                self.non_lorem[1].pk,
            ],
            url=url
        )

        # Search for: "chapter II" +(shutting | fender). Note, that `%2B`
        # stands for `+` symbol in the URL.
        self._search_boost(
            search_term='"chapter II" %2B(shutting | fender)',
            ordering=[
                self.non_lorem[2].pk,
                self.non_lorem[1].pk,
            ],
            url=url
        )

    @unittest.skipIf(condition=ELASTICSEARCH_GTE_6_0, reason="")
    def test_search_without_quotes_boost(self, url=None):
        """Search boost without quotes. Does not work on Elasticsearch 6.x.

        :return:
        """
        # Search for: Pig and Pepper
        self._search_boost(
            search_term='Pig and Pepper',
            ordering=[
                self.non_lorem[3].pk,
                self.non_lorem[4].pk,
            ],
            url=url
        )

    def test_search_with_quotes_alternative(self):
        """Test search by field.

        :param url:
        :return:
        """
        url = reverse(
            'bookdocument_simple_query_string_boost_search_backend-list',
            kwargs={}
        )
        return self.test_search_with_quotes(url)

    def test_search_with_quotes_boost_alternative(self):
        """Search boost.

        :return:
        """
        url = reverse(
            'bookdocument_simple_query_string_boost_search_backend-list',
            kwargs={}
        )
        return self.test_search_with_quotes_boost(url)

    def test_search_selected_fields(self, url=None):
        """Search boost.

        :return:
        """
        # Search for: "chapter II" +fender. Note, that `%2B` stands for `+`
        # symbol in the URL.
        self._search(
            search_term='title,summary:"Pool of Tears"',
            num_results=2,
            url=url
        )

    def test_search_boost_selected_fields(self, url=None):
        """Search boost.

        :return:
        """
        # Search for (only in `title` and `summary`): "Pool of Tears"
        self._search_boost(
            search_term='title,summary:"Pool of Tears"',
            ordering=[
                self.non_lorem[0].pk,
                self.non_lorem[1].pk,
            ],
            url=url
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
