"""
Test filtering backend.
"""

from __future__ import absolute_import

import unittest

from django.core.management import call_command

import pytest

from rest_framework import status

from books import constants

from .base import BaseRestFrameworkTestCase
from .data_mixins import AddressesMixin, BooksMixin

__title__ = 'django_elasticsearch_dsl_drf.tests.test_filtering'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestFilteringCommon',
)


@pytest.mark.django_db
class TestFilteringCommon(BaseRestFrameworkTestCase,
                          AddressesMixin,
                          BooksMixin):
    """Test filtering common."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up."""
        # Testing simple documents: Publisher index.
        cls.create_books()

        # Testing nested objects: Addresses, cities and countries
        cls.created_addresses()

        # Update the Elasticsearch index
        call_command('search_index', '--rebuild', '-f')

    # ***********************************************************************
    # ************************ Simple fields ********************************
    # ***********************************************************************

    def _field_filter_value(self, field_name, value, count):
        """Field filter value.

        Usage example:

            >>> self._field_filter_value(
            >>>     'title__wildcard',
            >>>     self.prefix[3:-3],
            >>>     self.prefix_count
            >>> )
        """
        url = self.base_url[:]
        data = {}
        response = self.client.get(
            url + '?{}={}'.format(field_name, value),
            data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data['results']),
            count
        )

    def _field_filter_term(self, field_name, filter_value):
        """Field filter term.

        Example:

            http://localhost:8000/api/articles/?tags=children
        """
        self.authenticate()

        url = self.base_url[:]
        data = {}

        # Should contain 22 results
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), self.all_count)

        # Should contain only 10 results
        filtered_response = self.client.get(
            url + '?{}={}'.format(field_name, filter_value),
            data
        )
        self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(filtered_response.data['results']),
            self.published_count
        )

    def test_field_filter_term(self):
        """Field filter term."""
        return self._field_filter_term(
            'state',
            constants.BOOK_PUBLISHING_STATUS_PUBLISHED
        )

    def test_field_filter_term_explicit(self):
        """Field filter term."""
        return self._field_filter_term(
            'state__term',
            constants.BOOK_PUBLISHING_STATUS_PUBLISHED
        )

    def test_field_filter_range(self):
        """Field filter range.

        Example:

            http://localhost:8000/api/users/?age__range=16|67
        """
        lower_id = self.published[0].id
        upper_id = self.published[-1].id
        value = '{}|{}'.format(lower_id, upper_id)
        return self._field_filter_value(
            'id__range',
            value,
            self.published_count
        )

    def test_field_filter_range_with_boost(self):
        """Field filter range.

        Example:

            http://localhost:8000/api/users/?age__range=16|67|2.0
        """
        lower_id = self.published[0].id
        upper_id = self.published[-1].id
        value = '{}|{}|{}'.format(lower_id, upper_id, '2.0')
        return self._field_filter_value(
            'id__range',
            value,
            self.published_count
        )

    def test_field_filter_prefix(self):
        """Test filter prefix.

        Example:

            http://localhost:8000/api/articles/?tags__prefix=bio
        """
        return self._field_filter_value(
            'title__prefix',
            self.prefix,
            self.prefix_count
        )

    def test_field_filter_in(self):
        """Test filter in.

        Example:

            http://localhost:8000/api/articles/?id__in=1|2|3
        """
        return self._field_filter_value(
            'id__in',
            '|'.join([str(__b.id) for __b in self.prefixed]),
            self.prefix_count
        )

    def _field_filter_terms_list(self, field_name, in_values, count):
        """Field filter terms.

        Example:

            http://localhost:8000/api/articles/?id=1&id=2&id=3
        """
        url = self.base_url[:]
        data = {}
        url_parts = ['{}={}'.format(field_name, val) for val in in_values]
        response = self.client.get(
            url + '?{}'.format('&'.join(url_parts)),
            data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data['results']),
            count
        )

    def test_field_filter_terms_list(self):
        """Test filter terms."""
        return self._field_filter_terms_list(
            'id',
            [str(__b.id) for __b in self.prefixed],
            self.prefix_count
        )

    def test_field_filter_terms_string(self):
        """Test filter terms.

        Example:

            http://localhost:8000/api/articles/?id__terms=1|2|3
        """
        return self._field_filter_value(
            'id__terms',
            '|'.join([str(__b.id) for __b in self.prefixed]),
            self.prefix_count
        )

    def test_field_filter_exists_true(self):
        """Test filter exists true.

        Example:

            http://localhost:8000/api/articles/?tags__exists=true
        """
        return self._field_filter_value(
            'tags__exists',
            'true',
            self.all_count
        )

    def test_field_filter_exists_false(self):
        """Test filter exists.

        Example:

            http://localhost:8000/api/articles/?non_existent__exists=false
        """
        return self._field_filter_value(
            'non_existent_field__exists',
            'false',
            self.all_count
        )

    def test_field_filter_wildcard(self):
        """Test filter wildcard.

        Example:

            http://localhost:8000/api/articles/?title__wildcard=*elusional*
        """
        return self._field_filter_value(
            'title__wildcard',
            '*{}*'.format(self.prefix[1:6]),
            self.prefix_count
        )

    def test_field_filter_exclude(self):
        """Test filter exclude.

        Example:

            http://localhost:8000/api/articles/?tags__exclude=children
        """
        return self._field_filter_value(
            'state__exclude',
            constants.BOOK_PUBLISHING_STATUS_PUBLISHED,
            self.all_count - self.published_count
        )

    def test_field_filter_isnull_true(self):
        """Test filter isnull true.

        Example:

            http://localhost:8000/api/articles/?null_field__isnull=true
        """
        self._field_filter_value(
            'null_field__isnull',
            'true',
            self.all_count
        )
        self._field_filter_value(
            'tags__isnull',
            'true',
            self.no_tags_count
        )

    def test_field_filter_isnull_false(self):
        """Test filter isnull true.

        Example:

            http://localhost:8000/api/articles/?tags__isnull=false
        """
        self._field_filter_value(
            'null_field__isnull',
            'false',
            0
        )
        self._field_filter_value(
            'tags__isnull',
            'false',
            self.all_count - self.no_tags_count
        )

    def test_field_filter_endswith(self):
        """Test filter endswith.

        Example:

            http://localhost:8000/api/articles/?state__endswith=lished
        """
        return self._field_filter_value(
            'state__endswith',
            constants.BOOK_PUBLISHING_STATUS_PUBLISHED[4:],
            self.published_count
        )

    def test_field_filter_contains(self):
        """Test filter contains.

        Example:

            http://localhost:8000/api/articles/?state__contains=lishe
        """
        return self._field_filter_value(
            'state__contains',
            constants.BOOK_PUBLISHING_STATUS_PUBLISHED[4:-2],
            self.published_count
        )

    def _field_filter_gte_lte(self, field_name, value, lookup, boost=None):
        """Field filter gt/gte/lt/lte.

        Example:

            http://localhost:8000/api/users/?id__gt=10
            http://localhost:8000/api/users/?id__gte=10
            http://localhost:8000/api/users/?id__lt=10
            http://localhost:8000/api/users/?id__lte=10
        """
        url = self.base_url[:]
        data = {}

        if boost is not None:
            url += '?{}__{}={}|{}'.format(field_name, lookup, value, boost)
        else:
            url += '?{}__{}={}'.format(field_name, lookup, value)

        response = self.client.get(
            url,
            data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        __mapping = {
            'gt': self.assertGreater,
            'gte': self.assertGreaterEqual,
            'lt': self.assertLess,
            'lte': self.assertLessEqual,
        }
        __func = __mapping.get(lookup)

        if callable(__func):
            for obj in response.data['results']:
                __func(
                    obj['id'],
                    value
                )

    def test_field_filter_gt(self):
        """Field filter gt.

        Example:

            http://localhost:8000/api/users/?id__gt=10
        :return:
        """
        return self._field_filter_gte_lte('id', self.in_progress[0].id, 'gt')

    def test_field_filter_gt_with_boost(self):
        """Field filter gt with boost.

        Example:

            http://localhost:8000/api/users/?id__gt=10|2.0
        :return:
        """
        # TODO: check boost value
        return self._field_filter_gte_lte(
            'id',
            self.in_progress[0].id,
            'gt',
            '2.0'
        )

    def test_field_filter_gte(self):
        """Field filter gte.

        Example:

            http://localhost:8000/api/users/?id__gte=10
        :return:
        """
        return self._field_filter_gte_lte('id', self.in_progress[0].id, 'gte')

    def test_field_filter_lt(self):
        """Field filter lt.

        Example:

            http://localhost:8000/api/users/?id__lt=10
        :return:
        """
        return self._field_filter_gte_lte('id', self.in_progress[0].id, 'lt')

    def test_field_filter_lt_with_boost(self):
        """Field filter lt with boost.

        Example:

            http://localhost:8000/api/users/?id__lt=10|2.0
        :return:
        """
        # TODO: check boost value
        return self._field_filter_gte_lte(
            'id',
            self.in_progress[0].id,
            'lt',
            '2.0'
        )

    def test_field_filter_lte(self):
        """Field filter lte.

        Example:

            http://localhost:8000/api/users/?id__lte=10
        :return:
        """
        return self._field_filter_gte_lte('id', self.in_progress[0].id, 'lte')

    def test_ids_filter(self):
        """Test ids filter.

        Example:

            http://localhost:8000/api/articles/?ids=68|64|58
            http://localhost:8000/api/articles/?ids=68&ids=64&ids=58
        """
        __ids = [str(__obj.id) for __obj in self.published]
        return self._field_filter_value(
            'ids',
            '|'.join(__ids),
            self.published_count
        )

    # ***********************************************************************
    # ************************ Nested fields ********************************
    # ***********************************************************************

    def _nested_field_filter_term(self, field_name, filter_value, count):
        """Nested field filter term.

        Example:

            http://localhost:8000/api/articles/?tags=children
        """
        self.authenticate()

        url = self.addresses_url[:]
        data = {}

        # Should contain only 32 results
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data['results']),
            self.all_addresses_count
        )

        # Should contain only 10 results
        filtered_response = self.client.get(
            url + '?{}={}'.format(field_name, filter_value),
            data
        )
        self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(filtered_response.data['results']),
            count
        )

    def test_nested_field_filter_term(self):
        """Nested field filter term."""
        self._nested_field_filter_term(
            'city',
            'Yerevan',
            self.addresses_in_yerevan_count
        )

        self._nested_field_filter_term(
            'country',
            'Armenia',
            self.addresses_in_yerevan_count
        )

        self._nested_field_filter_term(
            'city',
            'Dublin',
            self.addresses_in_dublin_count
        )

    def test_various_complex_fields(self):
        """Test various complex fields.

        :return:
        """
        data = {}
        response = self.client.get(self.cities_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.city_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


if __name__ == '__main__':
    unittest.main()
