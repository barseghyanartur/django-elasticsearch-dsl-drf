# coding: utf-8
"""
Test suggestions backend.
"""

from __future__ import absolute_import, unicode_literals

import unittest

from django.core.management import call_command

from nine.versions import DJANGO_GTE_1_10

import pytest

from rest_framework import status

import factories

from ..versions import (
    ELASTICSEARCH_GTE_5_0,
    ELASTICSEARCH_GTE_6_0,
    ELASTICSEARCH_GTE_7_0,
)
from .base import BaseRestFrameworkTestCase
from .data_mixins import AddressesMixin

if DJANGO_GTE_1_10:
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

__title__ = 'django_elasticsearch_dsl_drf.tests.test_suggesters'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestContextSuggesters',
    'TestSuggesters',
    'TestSuggestersEmptyIndex',
)


@pytest.mark.django_db
class TestSuggesters(BaseRestFrameworkTestCase, AddressesMixin):
    """Test suggesters."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up class."""
        super(TestSuggesters, cls).setUpClass()

        cls.publishers = []
        cls.publishers.append(
            factories.PublisherFactory(
                name='Addison–Wesley',
                city='Brighton & Hove',
                state_province='East Midlands',
                country='Armenia',
            )
        )
        cls.publishers.append(
            factories.PublisherFactory(
                name='Adis International',
                city='Bristol',
                state_province='East of England',
                country='Argentina',
            )
        )
        cls.publishers.append(
            factories.PublisherFactory(
                name='Atlantic Books',
                city='Cardiff',
                state_province='North East',
                country='Belgium',
            )
        )
        cls.publishers.append(
            factories.PublisherFactory(
                name='Atlas Press',
                city='Carlisle',
                state_province='North West',
                country='Belarus',
            )
        )
        cls.publishers.append(
            factories.PublisherFactory(
                name='Book League of America',
                city='Chelmsford',
                state_province='South East',
                country='Burkina Faso',
            )
        )
        cls.publishers.append(
            factories.PublisherFactory(
                name='Book Works',
                city='Chester',
                state_province='South West',
                country='Burundi',
            )
        )
        cls.publishers.append(
            factories.PublisherFactory(
                name='Booktrope',
                city='Chichester',
                state_province='West Midlands',
                country='Netherlands',
            )
        )

        cls.publishers_url = reverse(
            'publisherdocument-suggest',
            kwargs={}
        )

        cls.books = []
        cls.books.append(
            factories.BookFactory(
                title='Aaaaa Bbbb',
                summary='`Twas brillig, and the slithy toves '
                        'Did gyre and gimble in the wabe. '
                        'All mimsy were the borogoves '
                        'And the mome raths outgrabe.',
                publisher__name='Antares',
                publisher__country='Armenia',
            )
        )
        cls.books.append(
            factories.BookFactory(
                title='Aaaaa Cccc',
                summary='"Beware the Jabberwock, my son! '
                        'The jaws that bite, the claws that catch! '
                        'Beware the Jubjub bird, and shun '
                        'The frumious Bandersnatch!',
                publisher__name='Antares',
                publisher__country='Armenia',
            )
        )
        cls.books.append(
            factories.BookFactory(
                title='Aaaaa Dddd',
                summary='He took his vorpal sword in his hand,'
                        'Long time the manxome foe he sought --'
                        'So rested he by the Tumtum tree,'
                        'And stood awhile in thought.',
                publisher__name='Antares',
                publisher__country='Armenia',
            )
        )

        cls.books += factories.BookFactory.create_batch(
            10,
            publisher__name='Oxford University Press',
            publisher__city='Yerevan',
            publisher__state_province='Ararat',
            publisher__country='Ireland',
        )

        cls.books_url = reverse(
            'bookdocument-suggest',
            kwargs={}
        )

        cls.books_suggest_context_url = reverse(
            'bookdocument_frontend-suggest',
            kwargs={}
        )

        cls.authors = []
        cls.authors.append(
            factories.AuthorFactory(
                name='John Doe',
                salutation='Aaa Bbb',
            )
        )
        cls.authors.append(
            factories.AuthorFactory(
                name='Jane Doe',
                salutation='Aaa Ccc',
            )
        )
        cls.authors.append(
            factories.AuthorFactory(
                name='Armen Doe',
                salutation='Bbb Ccc',
            )
        )

        cls.authors_url = reverse(
            'authordocument-suggest',
            kwargs={}
        )

        cls.created_addresses()

        cls.sleep()
        call_command('search_index', '--rebuild', '-f')

    def _test_suggesters(self, test_data, url):
        """Test suggesters."""
        self.authenticate()

        data = {}

        for _suggester_field, _test_cases in test_data.items():

            for _test_case, _expected_results in _test_cases.items():
                _url = url + '?' + _suggester_field + '=' + _test_case
                # Check if response now is valid
                response = self.client.get(
                    _url,
                    data
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertIn(_suggester_field, response.data)
                _unique_options = list(set([
                    __o['text']
                    for __o
                    in response.data[_suggester_field][0]['options']
                ]))
                self.assertEqual(
                    len(_unique_options),
                    len(_expected_results),
                    (
                        _url,
                        _test_case,
                        _expected_results,
                        _unique_options
                    )
                )

    def test_suggesters_completion(self):
        """Test suggesters completion."""
        # Testing publishers
        test_data = {
            'name_suggest__completion': {
                'Ad': ['Addison–Wesley', 'Adis International'],
                'Atl': ['Atlantic Books', 'Atlas Press'],
                'Boo': ['Book League of America', 'Book Works', 'Booktrope'],
            },
            'country_suggest__completion': {
                'Arm': ['Armenia'],
                'Ar': ['Armenia', 'Argentina'],
                'Bel': ['Belgium', 'Belarus'],
                'Bur': ['Burkina Faso', 'Burundi'],
                'Net': ['Netherlands'],
                'Fra': [],
            }
        }
        # Testing default suggesters as well
        test_data.update(
            {
                'name_suggest': test_data['name_suggest__completion'],
                'country_suggest': test_data['country_suggest__completion'],
            }
        )
        self._test_suggesters(test_data, self.publishers_url)

        # Testing books
        test_data = {
            'title_suggest__completion': {
                'Aaa': ['Aaaaa Bbbb', 'Aaaaa Cccc', 'Aaaaa Dddd'],
                'Bbb': [],
            },
        }
        self._test_suggesters(test_data, self.books_url)

        # Testing authors
        test_data = {
            'salutation.suggest__completion': {
                'Aaa': ['Aaa Bbb', 'Aaa Ccc'],
                'Bbb': ['Bbb Ccc'],
                'Hhh': [],
            },
        }
        self._test_suggesters(test_data, self.authors_url)

    def test_suggesters_completion_no_args_provided(self):
        """Test suggesters completion with no args provided."""
        data = {}
        # Check if response now is valid
        response = self.client.get(self.publishers_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_suggesters_term(self):
        """Test suggesters term."""
        # Testing books
        test_data = {
            'summary_suggest__term': {
                'borogovse': ['borogov'],
                'Tumtus': ['tumtum'],
                'Jabberwok': ['jabberwock'],
                'tovse': ['tove', 'took', 'twas'],
            },
        }
        self._test_suggesters(test_data, self.books_url)

    def test_suggesters_phrase(self):
        """Test suggesters phrase."""
        # Testing books
        test_data = {
            'summary_suggest__phrase': {
                'slith tovs': ['slithi tov'],
                'mimsy boroto': ['mimsi borogov'],
            },
        }
        self._test_suggesters(test_data, self.books_url)

    def test_nested_fields_suggesters_completion(self):
        """Test suggesters completion for nested fields."""
        # Testing cities and countries
        test_data = {
            'city_suggest__completion': {
                'Ye': ['Yerevan', 'Yeovil'],
                'Yer': ['Yerevan'],
                'Ams': ['Amsterdam'],
                'Du': ['Dublin'],
                'Ne': [],
            },
            'country_suggest__completion': {
                'Arm': ['Armenia'],
                'Ar': ['Armenia', 'Argentina'],
                'Re': ['Republic of Ireland'],
                'Net': ['Netherlands'],
                'Fra': [],
            }
        }
        self._test_suggesters(test_data, self.addresses_suggest_url)


@pytest.mark.django_db
class TestSuggestersEmptyIndex(BaseRestFrameworkTestCase, AddressesMixin):
    """Test suggesters on empty index."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up class."""
        cls.authors_url = reverse(
            'authordocument-suggest',
            kwargs={}
        )

        cls.sleep()
        # Suggest on empty index
        call_command('search_index', '--delete', '-f')
        call_command('search_index', '--create', '-f')

    def test_suggesters_on_empty_index(self):
        """Test suggesters phrase."""
        response = self.client.get(
            self.authors_url + '?name_suggest__completion=Ad',
            {}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if ELASTICSEARCH_GTE_7_0:
            self.assertTrue(
                bool(response.data.get('name_suggest__completion'))
            )
        elif ELASTICSEARCH_GTE_6_0:
            self.assertFalse(bool(response.data))
        else:
            self.assertFalse(
                bool(response.data.get('name_suggest__completion'))
            )


@unittest.skipIf(not ELASTICSEARCH_GTE_5_0, 'ES >=5.x only')
@pytest.mark.django_db
class TestContextSuggesters(BaseRestFrameworkTestCase, AddressesMixin):
    """Test context suggesters."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up class."""
        # Books
        cls.books = []
        cls.books.append(
            factories.BookFactory(
                title='Ccccc Bbbb',
                summary='`Twas brillig, and the slithy toves '
                        'Did gyre and gimble in the wabe. '
                        'All mimsy were the borogoves '
                        'And the mome raths outgrabe.',
                publisher__name='Antares',
                publisher__country='Armenia',
            )
        )
        cls.books.append(
            factories.BookFactory(
                title='Ccccc Cccc',
                summary='"Beware the Jabberwock, my son! '
                        'The jaws that bite, the claws that catch! '
                        'Beware the Jubjub bird, and shun '
                        'The frumious Bandersnatch!',
                publisher__name='Antares',
                publisher__country='Armenia',
            )
        )
        cls.books.append(
            factories.BookFactory(
                title='Ccccc Dddd',
                summary='He took his vorpal sword in his hand,'
                        'Long time the manxome foe he sought --'
                        'So rested he by the Tumtum tree,'
                        'And stood awhile in thought.',
                publisher__name='Antares',
                publisher__country='Armenia',
            )
        )
        cls.books.append(
            factories.BookFactory(
                title='Ccccc Eeee',
                summary='She took his zorpal blade in his hand,'
                        'Long time the manxome foe he sought --'
                        'So rested he by the Tumtum tree,'
                        'And stood awhile in thought.',
                # publisher__name='Mario',
                # publisher__country='US',
            )
        )

        cls.books += factories.BookFactory.create_batch(
            10,
            publisher__name='Oxford University Press',
            publisher__city='Yerevan',
            publisher__state_province='Ararat',
            publisher__country='Ireland',
        )

        cls.books_suggest_context_url = reverse(
            'bookdocument_frontend-suggest',
            kwargs={}
        )

        # Addresses
        cls.addresses = []
        cls.addresses.append(
            factories.AddressFactory(
                street='Halabyan',
                city__name='Yerevan',
                latitude=40.0742719,
                longitude=44.1930605,
            )
        )
        cls.addresses.append(
            factories.AddressFactory(
                street='Hambardzumyan',
                city__name='Yerevan',
                latitude=40.01,
                longitude=44.01,
            )
        )
        cls.addresses.append(
            factories.AddressFactory(
                street='Haghartsin',
                city__name='Yerevan',
                latitude=39.92,
                longitude=43.92,
            )
        )
        cls.addresses.append(
            factories.AddressFactory(
                street='Hamazaspyan',
                city__name='Tatev',
                latitude=39.3793612,
                longitude=46.2480006,
            )
        )
        cls.addresses.append(
            factories.AddressFactory(
                street='Harazatyan',
                city__name='Tatev',
                latitude=39.3793612,
                longitude=46.2480006,
            )
        )
        cls.addresses.append(
            factories.AddressFactory(
                street='Hardewijk',
                city__name='Groningen',
                latitude=53.2246892,
                longitude=6.56429,
            )
        )
        cls.addresses.append(
            factories.AddressFactory(
                street='Haringstraat',
                city__name='Groningen',
                latitude=53.2246892,
                longitude=6.56429,
            )
        )

        cls.addresses_suggest_context_url = reverse(
            'addressdocument_frontend-suggest',
            kwargs={}
        )

        cls.sleep()
        call_command('search_index', '--rebuild', '-f')

    def _test_suggesters_completion_context(self, test_data, url):
        """Test suggesters completion context."""
        self.authenticate()

        data = {}

        for _suggester_field, _test_cases in test_data.items():

            for _test_case, _test_data in _test_cases.items():
                _url = url + '?' + _suggester_field + '=' + _test_case
                for _query_param, _value in _test_data['filters'].items():
                    _url += '&{}={}'.format(_query_param, _value)
                # Check if response now is valid
                response = self.client.get(
                    _url,
                    data
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertIn(_suggester_field, response.data)
                _unique_options = list(set([
                    __o['text']
                    for __o
                    in response.data[_suggester_field][0]['options']
                ]))
                self.assertEqual(
                    len(_unique_options),
                    len(_test_data['expected_results']),
                    (
                        _url,
                        _test_case,
                        _test_data['expected_results'],
                        _unique_options
                    )
                )

    def test_suggesters_completion_context(self):
        """Test suggesters completion context."""
        # Testing books
        test_data = {
            'title_suggest_context': {
                'Ccc': {
                    'expected_results': [
                        'Ccccc Bbbb',
                        'Ccccc Cccc',
                        'Ccccc Dddd',
                    ],
                    'filters': {
                        'title_suggest_publisher': 'Antares',
                    }
                },
            },
        }
        self._test_suggesters_completion_context(
            test_data,
            self.books_suggest_context_url
        )

        # Testing addresses
        test_data = {
            'street_suggest_context': {
                'Ha': {
                    'expected_results': [
                        'Halabyan',
                        'Hambardzumyan',
                        'Haghartsin',
                        'Hamazaspyan',
                        'Harazatyan',
                    ],
                    'filters': {
                        'title_suggest_loc': (
                            '40__44__1000km'
                            if ELASTICSEARCH_GTE_6_0
                            else '40__44'
                        ),
                    }
                },
            },
        }
        self._test_suggesters_completion_context(
            test_data,
            self.addresses_suggest_context_url
        )


if __name__ == '__main__':
    unittest.main()
