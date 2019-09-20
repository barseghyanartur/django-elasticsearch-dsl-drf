"""
Test search backend.
"""

from __future__ import absolute_import

from time import sleep
import unittest

from django.core.management import call_command

from nine.versions import DJANGO_GTE_1_10

import pytest

from rest_framework import status

from books import constants
import factories
from search_indexes.viewsets import BookDocumentViewSet
from ..constants import SEPARATOR_LOOKUP_NAME
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
__copyright__ = '2017-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestSearch',
    'TestSearchCustomCases',
)


@pytest.mark.django_db
class TestSearch(BaseRestFrameworkTestCase):
    """Test search."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        super(TestSearch, cls).setUpClass()

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

        cls.cities = list(set(factories.DutchCityFactory.create_batch(100)))
        cls.cities_count = len(cls.cities)

        # Create 10 cities in a given country. The reason that we don't
        # do create_batch here is that sometimes in the same test city name is
        # generated twice and thus our concept of precise number matching
        # fails. Before there's a better approach, this would stay so. The
        # create_batch part (below) will remain commented out, until there's a
        # better solution.
        cls.switzerland = factories.CountryFactory.create(name='Wonderland')
        cls.switz_cities_names = factories.SWISS_CITIES

        cls.switz_cities = list(
            set(
                factories.SwissCityFactory.create_batch(
                    size=100,
                    country=cls.switzerland
                )
            )
        )
        cls.switz_cities_count = len(cls.switz_cities)
        # cls.switz_cities = factories.CityFactory.create_batch(
        #     cls.switz_cities_count,
        #     country=cls.switzerland
        # )
        cls.all_cities_count = cls.cities_count + cls.switz_cities_count

        call_command('search_index', '--rebuild', '-f')

        # Testing coreapi and coreschema
        cls.backend = SearchFilterBackend()
        cls.view = BookDocumentViewSet()

    def _search_by_field(self,
                         search_term,
                         num_results,
                         url=None,
                         search_field='search'):
        """Search by field."""
        self.authenticate()

        if url is None:
            url = reverse('bookdocument-list', kwargs={})
        data = {}

        # Should contain 20 results
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), self.all_count)

        if isinstance(search_term, (list, tuple)):
            _query_string = []
            for _search_term in search_term:
                _query_string.append(
                    '{}={}'.format(search_field, _search_term)
                )
            filtered_url = url + '?' + '&'.join(_query_string)
        else:
            # Should contain only `num_results` results
            filtered_url = url + '?search={}'.format(search_term)

        filtered_response = self.client.get(filtered_url, data)
        self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(filtered_response.data['results']),
            num_results
        )

    def _search_boost(self,
                      search_term,
                      ordering,
                      url=None,
                      search_field='search'):
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
            url = reverse('bookdocument_ordered_by_score-list', kwargs={})
        data = {}

        filtered_response = self.client.get(
            url + '?{}={}'.format(search_field, search_term),
            data
        )
        self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)
        self.assertIn('results', filtered_response.data)
        for counter, item_id in enumerate(ordering):
            result_item = filtered_response.data['results'][counter]
            self.assertEqual(result_item['id'], item_id)

    def test_search_boost(self, url=None, search_field='search'):
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
            ],
            url=url,
            search_field=search_field
        )

        # Search for "Pig and Pepper"
        self._search_boost(
            search_term="Pig and Pepper",
            ordering=[
                self.non_lorem[3].pk,
                self.non_lorem[4].pk,
                self.non_lorem[5].pk,
            ],
            url=url,
            search_field=search_field
        )

        # Search for "Who Stole the Tarts"
        self._search_boost(
            search_term="Who Stole the Tarts",
            ordering=[
                self.non_lorem[6].pk,
                self.non_lorem[7].pk,
                self.non_lorem[8].pk,
            ],
            url=url,
            search_field=search_field
        )

    def test_search_boost_compound(self, search_field='search'):
        url = reverse(
            'bookdocument_compound_search_backend_ordered_by_score-list',
            kwargs={}
        )
        return self.test_search_boost(url=url, search_field=search_field)

    def _search_by_nested_field(self,
                                search_term,
                                url=None,
                                search_field='search'):
        """Search by field."""
        self.authenticate()

        if url is None:
            url = reverse('citydocument-list', kwargs={})

        data = {}

        # Should contain 20 results
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), self.all_cities_count)

        # Should contain only 10 results
        filtered_response = self.client.get(
            url + '?{}={}'.format(search_field, search_term),
            data
        )
        self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(filtered_response.data['results']),
            self.switz_cities_count
        )

    def test_search_by_field(self, url=None, search_field='search'):
        """Search by field."""
        self._search_by_field(
            search_term='photography',
            num_results=self.special_count,
            url=url,
            search_field=search_field
        )
        self._search_by_field(
            search_term='summary{}photography'.format(SEPARATOR_LOOKUP_NAME),
            num_results=self.special_count,
            url=url,
            search_field=search_field
        )

    def test_search_by_field_multi_terms(self,
                                         url=None,
                                         search_field='search'):
        """Search by field, multiple terms."""
        self._search_by_field(
            search_term=['photography', 'art'],
            num_results=self.special_count,
            url=url,
            search_field=search_field
        )
        self._search_by_field(
            search_term=[
                'summary{}photography'.format(SEPARATOR_LOOKUP_NAME),
                'summary{}art'.format(SEPARATOR_LOOKUP_NAME)
            ],
            num_results=self.special_count,
            url=url,
            search_field=search_field
        )

    def test_compound_search_by_field(self):
        url = reverse('bookdocument_compound_search_backend-list', kwargs={})
        self.test_search_by_field(url=url)

    def test_compound_search_boost_by_field(self):
        url = reverse(
            'bookdocument_compound_search_boost_backend-list', kwargs={}
        )
        self.test_search_by_field(url=url)

    def test_compound_search_by_field_multi_terms(self):
        url = reverse('bookdocument_compound_search_backend-list', kwargs={})
        return self.test_search_by_field_multi_terms(url=url)

    def test_search_by_nested_field(self, url=None):
        """Search by field."""
        self._search_by_nested_field(
            'Wonderland',
            url=url
        )
        # self._search_by_nested_field(
        #     'name{}Wonderland'.format(SEPARATOR_LOOKUP_NAME),
        #     url=url
        # )

    def test_compound_search_by_nested_field(self):
        url = reverse('citydocument_compound_search_backend-list', kwargs={})
        return self.test_search_by_nested_field(url=url)

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


@pytest.mark.django_db
class TestSearchCustomCases(BaseRestFrameworkTestCase):
    """Test search."""

    pytestmark = pytest.mark.django_db

    def _reindex(self):
        call_command('search_index', '--rebuild', '-f')

    def _test_search_any_word_in_indexed_fields(self,
                                                search_term,
                                                url,
                                                expected_num_results,
                                                title_match=None,
                                                create_factory=False):
        if create_factory:
            factories.BookWithUniqueTitleFactory(
                title='This is a short indexed description'
            )
            factories.BookWithUniqueTitleFactory.create_batch(100)
            self._reindex()

        self.authenticate()
        filtered_url = url + '?search={}'.format(search_term)
        filtered_response = self.client.get(filtered_url)
        self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(filtered_response.data['results']),
            expected_num_results
        )
        if title_match:
            self.assertEqual(
                filtered_response.data['results'][0]['title'],
                title_match
            )

    def test_search_any_word_in_indexed_fields(self):
        """Test search any word in indexed fields.

        :return:
        """
        # Create some data to test
        book = factories.BookWithUniqueTitleFactory(
            title='This is a short indexed description'
        )
        factories.BookWithUniqueTitleFactory.create_batch(100)
        self._reindex()
        sleep(3)  # Wait until indexed
        url = reverse('bookdocument-list', kwargs={})

        self._test_search_any_word_in_indexed_fields(
            search_term='short indexed description',
            url=url,
            expected_num_results=1,
            title_match=book.title,
            create_factory=False
        )
        self._test_search_any_word_in_indexed_fields(
            search_term='a description',
            url=url,
            expected_num_results=1,
            title_match=book.title,
            create_factory=False
        )

        self._test_search_any_word_in_indexed_fields(
            search_term='short description',
            url=url,
            expected_num_results=1,
            title_match=book.title,
            create_factory=False
        )


if __name__ == '__main__':
    unittest.main()
