# coding: utf-8
"""
Test functional suggestions backend.
"""

from __future__ import absolute_import, unicode_literals

import unittest

from django.core.management import call_command

from nine.versions import DJANGO_GTE_1_10

import pytest

from rest_framework import status

import factories

from .base import BaseRestFrameworkTestCase
from .data_mixins import AddressesMixin

if DJANGO_GTE_1_10:
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

__title__ = 'django_elasticsearch_dsl_drf.tests.test_suggesters'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestFunctionalSuggesters',
)


@pytest.mark.django_db
class TestFunctionalSuggesters(BaseRestFrameworkTestCase, AddressesMixin):
    """Test functional suggesters."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up class."""
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
                name='Strip Books of America',
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
            'publisherdocument-functional-suggest',
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
        cls.books.append(
            factories.BookFactory(
                title='Eeeee Ffff',
                summary='He took his vorpal sword in his hand,'
                        'Long time the manxome foe he sought --'
                        'So rested he by the Tumtum tree,'
                        'And stood awhile in thought.',
                publisher__name='Strip Books of America',
                publisher__country='Burkina Faso',
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
            'bookdocument_functional_suggester-functional-suggest',
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
            'authordocument-functional-suggest',
            kwargs={}
        )

        cls.created_addresses()

        call_command('search_index', '--rebuild', '-f')

    def _test_suggesters(self, test_data, url):
        """Test suggesters."""
        self.authenticate()

        data = {}

        for _suggester_field, _test_cases in test_data.items():

            for _test_case, _expected_results in _test_cases.items():
                # Check if response now is valid
                response = self.client.get(
                    url + '?' + _suggester_field + '=' + _test_case,
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
                    (_test_case, _expected_results)
                )
                self.assertEqual(
                    sorted(_unique_options),
                    sorted(_expected_results),
                    (_test_case, _expected_results)
                )

    def test_suggesters_completion(self):
        """Test suggesters completion."""
        # Testing publishers
        test_data = {
            'name_suggest__completion_prefix': {
                'Ad': ['Addison–Wesley', 'Adis International'],
                'Atl': ['Atlantic Books', 'Atlas Press'],
                'Boo': ['Book League of America', 'Book Works', 'Booktrope'],
                'Stri': ['Strip Books of America'],
            },
            'name_match_suggest__completion_match': {
                'Strip': ['Strip Books of America', ],
                'America': [
                    'Strip Books of America',
                    'Book League of America',
                ],
            },
            'country_suggest__completion_prefix': {
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
                'name_suggest': test_data['name_suggest__completion_prefix'],
                'name_match_suggest':
                    test_data['name_match_suggest__completion_match'],
                'country_suggest':
                    test_data['country_suggest__completion_prefix'],
            }
        )
        self._test_suggesters(test_data, self.publishers_url)

        # Testing books
        test_data = {
            'title_suggest_prefix__completion_prefix': {
                'Aaa': ['Aaaaa Bbbb', 'Aaaaa Cccc', 'Aaaaa Dddd'],
                'Bbb': [],
            },
        }
        # Testing default suggesters as well
        test_data.update(
            {
                'title_suggest_prefix':
                    test_data['title_suggest_prefix__completion_prefix'],
                'title.raw__completion_prefix':
                    test_data['title_suggest_prefix__completion_prefix'],
                'title_simple__completion_prefix':
                    test_data['title_suggest_prefix__completion_prefix'],
            }
        )
        self._test_suggesters(test_data, self.books_url)

        # Testing authors
        test_data = {
            'salutation_suggest__completion_prefix': {
                'Aaa': ['Aaa Bbb', 'Aaa Ccc'],
                'Bbb': ['Bbb Ccc'],
                'Hhh': [],
            },
        }
        # Testing default suggesters as well
        test_data.update(
            {
                'salutation_suggest':
                    test_data['salutation_suggest__completion_prefix'],
                'salutation.raw':
                    test_data['salutation_suggest__completion_prefix'],
            }
        )
        self._test_suggesters(test_data, self.authors_url)

    def test_suggesters_completion_no_args_provided(self):
        """Test suggesters completion with no args provided."""
        data = {}
        # Check if response now is valid
        response = self.client.get(self.publishers_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_suggesters_term(self):
    #     """Test suggesters term."""
    #     # Testing books
    #     test_data = {
    #         'summary_suggest__term': {
    #             'borogovse': ['borogov'],
    #             'Tumtus': ['tumtum'],
    #             'Jabberwok': ['jabberwock'],
    #             'tovse': ['tove', 'took', 'twas'],
    #         },
    #     }
    #     self._test_suggesters(test_data, self.books_url)
    #
    # def test_suggesters_phrase(self):
    #     """Test suggesters phrase."""
    #     # Testing books
    #     test_data = {
    #         'summary_suggest__phrase': {
    #             'slith tovs': ['slithi tov'],
    #             'mimsy boroto': ['mimsi borogov'],
    #         },
    #     }
    #     self._test_suggesters(test_data, self.books_url)
    #
    # def test_nested_fields_suggesters_completion(self):
    #     """Test suggesters completion for nested fields."""
    #     # Testing cities and countries
    #     test_data = {
    #         'city_suggest__completion': {
    #             'Ye': ['Yerevan', 'Yeovil'],
    #             'Yer': ['Yerevan'],
    #             'Ams': ['Amsterdam'],
    #             'Du': ['Dublin'],
    #             'Ne': [],
    #         },
    #         'country_suggest__completion': {
    #             'Arm': ['Armenia'],
    #             'Ar': ['Armenia', 'Argentina'],
    #             'Re': ['Republic of Ireland'],
    #             'Net': ['Netherlands'],
    #             'Fra': [],
    #         }
    #     }
    #     self._test_suggesters(test_data, self.addresses_suggest_url)


if __name__ == '__main__':
    unittest.main()
