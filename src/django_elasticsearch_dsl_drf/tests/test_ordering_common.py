"""
Test ordering backend.
"""

from __future__ import absolute_import

from six.moves import reduce

import unittest

from django.core.management import call_command
from django.urls import reverse

import pytest

from rest_framework import status

from django_elasticsearch_dsl_drf.filter_backends import OrderingFilterBackend

import factories
from search_indexes.viewsets import BookDocumentViewSet

from .base import (
    BaseRestFrameworkTestCase,
    CORE_API_AND_CORE_SCHEMA_ARE_INSTALLED,
    CORE_API_AND_CORE_SCHEMA_MISSING_MSG,
)

__title__ = 'django_elasticsearch_dsl_drf.tests.test_ordering'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestOrdering',
)


@pytest.mark.django_db
class TestOrdering(BaseRestFrameworkTestCase):
    """Test ordering."""

    pytestmark = pytest.mark.django_db

    @staticmethod
    def deep_get(dic, keys, default=None):
        """Returns value at period separated keys in dictionary or default

        From https://stackoverflow.com/a/46890853

        :param dic: Dictionary to retrieve value from.
        :param keys: Period separated path of keys
        :param default: Default value to return if keys not found
        :type dic: dict
        :type keys: str
        :type default: str
        :return: Value at keys or default
        """
        return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict)
                      else default, keys.split("."), dic)

    @classmethod
    def setUpClass(cls):
        """Set up class."""
        super(TestOrdering, cls).setUpClass()

        cls.address_in_sydney = factories.AddressFactory.create(
            **{
                'city__name': 'Sydney',
                'city__country__name': 'Australia',
                'city__country__continent__name': 'Australia',
            }
        )
        cls.address_in_buenos_aires = factories.AddressFactory.create(
            **{
                'city__name': 'Buenos Aires',
                'city__country__name': 'Argentina',
                'city__country__continent__name': 'South America',
            }
        )
        cls.address_in_new_york = factories.AddressFactory.create(
            **{
                'city__name': 'New York',
                'city__country__name': 'USA',
                'city__country__continent__name': 'North America',
            }
        )
        cls.address_in_yeovil = factories.AddressFactory.create(
            **{
                'city__name': 'Yeovil',
                'city__country__name': 'United Kingdom',
                'city__country__continent__name': 'Europe',
            }
        )
        cls.addresses_url = reverse('addressdocument-list', kwargs={})

        cls.books = factories.BookWithUniqueTitleFactory.create_batch(20)
        cls.books_url = reverse('bookdocument-list', kwargs={})

        cls.authors = factories.AuthorWithUniqueNameFactory.create_batch(20)
        cls.authors_url = reverse('authordocument-list', kwargs={})

        cls.sleep()
        call_command('search_index', '--rebuild', '-f')

        # Testing coreapi and coreschema
        cls.backend = OrderingFilterBackend()
        cls.view = BookDocumentViewSet()

    def _order_by_field(self,
                        field_name,
                        url,
                        check_ordering=True,
                        nested_resp_key=None):
        """Order by field.

        For testing the ``OrderingFilterBackend``.

        :param field_name:
        :param url:
        :param check_ordering:
        :param nested_resp_key:
        :type field_name: str
        :type url: str
        :type check_ordering: bool
        :type nested_resp_key: str
        :return: None
        """
        self.authenticate()

        data = {}

        # Just a plan field name without ordering information
        __f_name = field_name
        __assert_func = self.assertLess

        if field_name.startswith('-'):
            __f_name = field_name[1:]
            __assert_func = self.assertGreater

        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        filtered_response = self.client.get(
            url + '?ordering={}'.format(field_name),
            data
        )
        self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)

        if check_ordering:
            item_count = len(filtered_response.data['results'])

            for counter, item in enumerate(filtered_response.data['results']):
                if (counter > 1) and (counter < item_count + 1):
                    if nested_resp_key is not None:
                        __assert_func(
                            self.deep_get(
                                filtered_response.data['results'][counter-1],
                                nested_resp_key),
                            self.deep_get(
                                filtered_response.data['results'][counter],
                                nested_resp_key),
                        )
                    else:
                        __assert_func(
                            filtered_response.data['results'][counter-1][
                                __f_name],
                            filtered_response.data['results'][counter][
                                __f_name]
                        )

    def _order_by_default_field(self, field_name, url, check_ordering=True,
                                nested=False):
        """Order by default field.

        For testing the ``DefaultOrderingFilterBackend``.

        :param field_name:
        :param url:
        :param check_ordering:
        :param nested:
        :type field_name: str
        :type url: str
        :type check_ordering: bool
        :type nested: bool
        :return: None
        """
        self.authenticate()

        data = {}

        # Just a plan field name without ordering information
        __f_name = field_name
        __assert_func = self.assertLess

        if field_name.startswith('-'):
            __f_name = field_name[1:]
            __assert_func = self.assertGreater

        # Should contain 20 results
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if check_ordering:
            item_count = len(response.data['results'])

            for counter, item in enumerate(response.data['results']):
                if (counter > 1) and (counter < item_count + 1):
                    if nested:
                        __assert_func(
                            self.deep_get(
                                response.data['results'][counter - 1],
                                __f_name),
                            self.deep_get(response.data['results'][counter],
                                          __f_name),
                        )
                    else:
                        __assert_func(
                            response.data['results'][counter - 1][__f_name],
                            response.data['results'][counter][__f_name]
                        )

    def test_book_order_by_field_id_ascending(self):
        """Order by field `id` ascending."""
        return self._order_by_field('id', self.books_url)

    def test_book_order_by_field_id_descending(self):
        """Order by field `id` descending."""
        return self._order_by_field('-id', self.books_url)

    def test_book_order_by_field_title_ascending(self):
        """Order by field `title` ascending."""
        return self._order_by_field('title', self.books_url)

    def test_book_order_by_field_title_descending(self):
        """Order by field `title` descending."""
        return self._order_by_field('-title', self.books_url)

    def test_book_default_order_by(self):
        """Book order by default."""
        return self._order_by_default_field('id', self.books_url)

    def test_author_order_by_field_id_ascending(self):
        """Order by field `name` ascending."""
        return self._order_by_field('id', self.authors_url)

    def test_author_order_by_field_id_descending(self):
        """Order by field `id` descending."""
        return self._order_by_field('-id', self.authors_url)

    def test_author_order_by_field_name_ascending(self):
        """Order by field `name` ascending."""
        return self._order_by_field('name', self.authors_url)

    def test_author_order_by_field_name_descending(self):
        """Order by field `name` descending."""
        return self._order_by_field('-name', self.authors_url)

    def test_author_default_order_by(self):
        """Author order by default."""
        return self._order_by_default_field('name', self.authors_url)

    def test_book_order_by_non_existent_field(self):
        """Order by non-existent field."""
        return self._order_by_field('another_non_existent_field',
                                    self.books_url,
                                    check_ordering=False)

    def test_address_default_order_by(self):
        """Test if default ordering on addresses is correct (asc)."""
        return self._order_by_default_field('id', self.addresses_url)

    # def test_address_default_order_by_descending(self):
    #     """Test if default ordering on ??? is correct (desc)."""
    #     # TODO: Define an endpoint where default ordering would be
    #     # desc and test on that.
    #     return self._order_by_default_field('-id', self.addresses_url)

    def test_address_default_nested_order_by(self):
        return self._order_by_default_field('city.name', self.addresses_url,
                                            nested=True)

    def test_address_order_by_nested_field_country_ascending(self):
        """Order by field `continent.country.name.raw` ascending."""
        return self._order_by_field('country', self.addresses_url,
                                    nested_resp_key='country.name')

    def test_address_order_by_nested_field_country_descending(self):
        """Order by field `continent.country.name.raw` descending."""
        return self._order_by_field('-country', self.addresses_url,
                                    nested_resp_key='country.name')

    def test_address_order_by_nested_field_continent_ascending(self):
        """Order by field `continent.country.name.raw` ascending."""
        return self._order_by_field('continent', self.addresses_url,
                                    nested_resp_key='continent.name')

    def test_address_order_by_nested_field_continent_descending(self):
        """Order by field `continent.country.name.raw` descending."""
        return self._order_by_field('-continent', self.addresses_url,
                                    nested_resp_key='continent.name')

    @unittest.skipIf(not CORE_API_AND_CORE_SCHEMA_ARE_INSTALLED,
                     CORE_API_AND_CORE_SCHEMA_MISSING_MSG)
    def test_schema_fields_with_filter_fields_list(self):
        """Test schema field generator"""
        fields = self.backend.get_schema_fields(self.view)
        fields = [f.name for f in fields]
        self.assertEqual(fields, ['ordering'])

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
