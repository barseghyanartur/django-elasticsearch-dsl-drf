"""
Test nested filtering backend.
"""

from __future__ import absolute_import

import copy
import unittest

from django.core.management import call_command

import pytest

from rest_framework import status

from search_indexes.viewsets import AddressDocumentViewSet

from ..constants import SEPARATOR_LOOKUP_COMPLEX_VALUE
from ..filter_backends import NestedFilteringFilterBackend
from .base import (
    BaseRestFrameworkTestCase,
    CORE_API_AND_CORE_SCHEMA_ARE_INSTALLED,
    CORE_API_AND_CORE_SCHEMA_MISSING_MSG,
)
from .data_mixins import AddressesMixin

__title__ = 'django_elasticsearch_dsl_drf.tests.test_filtering_nested'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestFilteringNested',
)


@pytest.mark.django_db
class TestFilteringNested(BaseRestFrameworkTestCase, AddressesMixin):
    """Test filtering nested."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up."""
        # Testing nested objects: Addresses, cities and countries, continents
        cls.created_addresses()

        cls.all_addresses = (
            cls.addresses_in_yerevan +
            cls.addresses_in_amsterdam +
            cls.addresses_in_dublin +
            cls.addresses_in_yeovil +
            cls.addresses_in_buenos_aires
        )
        cls.all_addresses_ids = sorted(
            set([obj.id for obj in cls.all_addresses])
        )
        cls.all_cities_ids = sorted(
            set([obj.city.id for obj in cls.all_addresses])
        )
        cls.add_addresses_dict = {
            cls.addresses_in_yerevan[0].city.id: {
                'count': len(cls.addresses_in_yerevan),
                'objects': cls.addresses_in_yerevan
            },
            cls.addresses_in_amsterdam[0].city.id: {
                'count': len(cls.addresses_in_amsterdam),
                'objects': cls.addresses_in_amsterdam
            },
            cls.addresses_in_dublin[0].city.id: {
                'count': len(cls.addresses_in_dublin),
                'objects': cls.addresses_in_dublin
            },
            cls.addresses_in_yeovil[0].city.id: {
                'count': len(cls.addresses_in_yeovil),
                'objects': cls.addresses_in_yeovil
            },
            cls.addresses_in_buenos_aires[0].city.id: {
                'count': len(cls.addresses_in_buenos_aires),
                'objects': cls.addresses_in_buenos_aires,
            }
        }

        # Update the Elasticsearch index
        call_command('search_index', '--rebuild', '-f')

        # Testing coreapi and coreschema
        cls.backend = NestedFilteringFilterBackend()
        cls.view = AddressDocumentViewSet()

    @property
    def base_url(self):
        return self.addresses_url

    # ***********************************************************************
    # ************************ Simple fields ********************************
    # ***********************************************************************

    def _field_filter_value(self, field_name, value, count):
        """Field filter value.

        Usage example:

            >>> self._field_filter_value(
            >>>     'continent_country_city__contains',
            >>>     'ere',
            >>>     self.addresses_in_yerevan_count
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

    def _field_filter_term(self,
                           field_name,
                           filter_value,
                           total_num_results,
                           filtered_num_results):
        """Field filter term.

        Example:

            http://localhost:8000/api/articles/?tags=children
        """
        self.authenticate()

        url = self.base_url[:]
        data = {}

        # Should contain `total_num_results` results
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), total_num_results)

        # Should contain only `filtered_num_results` results
        filtered_response = self.client.get(
            url + '?{}={}'.format(field_name, filter_value),
            data
        )
        self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(filtered_response.data['results']),
            filtered_num_results
        )

    def test_field_filter_term(self):
        """Field filter term."""
        return self._field_filter_term(
            'continent_country_city',
            'Yerevan',
            self.all_addresses_count,
            self.addresses_in_yerevan_count
        )

    def test_field_filter_term_explicit(self):
        """Field filter term."""
        return self._field_filter_term(
            'continent_country_city__term',
            'Yerevan',
            self.all_addresses_count,
            self.addresses_in_yerevan_count
        )

    def test_field_filter_range(self):
        """Field filter range.

        Example:

            http://localhost:8000/api/users/?age__range=16__67
        """
        # Pick the first and the last elements from the list
        lower_id = self.all_cities_ids[1]
        upper_id = self.all_cities_ids[3]
        value = '{lower_id}{sep}{upper_id}'.format(
            lower_id=lower_id,
            upper_id=upper_id,
            sep=SEPARATOR_LOOKUP_COMPLEX_VALUE
        )
        # Calculate expected number of items
        count = (
            self.add_addresses_dict[lower_id]['count'] +
            self.add_addresses_dict[lower_id + 1]['count'] +
            self.add_addresses_dict[upper_id]['count']
        )
        return self._field_filter_value(
            'continent_country_city_id__range',
            value,
            count
        )

    def test_field_filter_range_with_boost(self):
        """Field filter range.

        Example:

            http://localhost:8000/api/users/?age__range=16__67__2.0
        """
        lower_id = self.all_cities_ids[2]
        upper_id = self.all_cities_ids[4]
        value = '{lower_id}{sep}{upper_id}{sep}{boost}'.format(
            lower_id=lower_id,
            upper_id=upper_id,
            boost='2.0',
            sep=SEPARATOR_LOOKUP_COMPLEX_VALUE
        )
        # Calculate expected number of items
        count = (
                self.add_addresses_dict[lower_id]['count'] +
                self.add_addresses_dict[lower_id + 1]['count'] +
                self.add_addresses_dict[upper_id]['count']
        )
        return self._field_filter_value(
            'continent_country_city_id__range',
            value,
            count
        )

    def test_field_filter_prefix(self):
        """Test filter prefix.

        Example:

            http://localhost:8000/api/articles/?tags__prefix=bio
        """
        return self._field_filter_value(
            'continent_country_city__prefix',
            'Ye',  # Matches Yerevan and Yeovil
            self.addresses_in_yeovil_count + self.addresses_in_yerevan_count
        )

    def test_field_filter_in(self):
        """Test filter in.

        Example:

            http://localhost:8000/api/articles/?id__in=1__2__3
        """
        ids = [
            self.addresses_in_yerevan[0].city.id,
            self.addresses_in_amsterdam[0].city.id,
        ]
        return self._field_filter_value(
            'continent_country_city_id__in',
            SEPARATOR_LOOKUP_COMPLEX_VALUE.join([str(_id) for _id in ids]),
            self.addresses_in_amsterdam_count + self.addresses_in_yerevan_count
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
            'continent_country_city',
            ['Yerevan', 'Amsterdam'],
            self.addresses_in_amsterdam_count + self.addresses_in_yerevan_count
        )

    def test_field_filter_terms_string(self):
        """Test filter terms.

        Example:

            http://localhost:8000/api/articles/?id__terms=1__2__3
        """
        return self._field_filter_value(
            'continent_country_city__terms',
            SEPARATOR_LOOKUP_COMPLEX_VALUE.join(['Yerevan', 'Dublin']),
            self.addresses_in_dublin_count + self.addresses_in_yerevan_count
        )

    def test_field_filter_exists_true(self):
        """Test filter exists true.

        Example:

            http://localhost:8000/api/articles/?tags__exists=true
        """
        return self._field_filter_value(
            'continent_country_city__exists',
            'true',
            self.all_addresses_count
        )

    def test_field_filter_exists_false(self):
        """Test filter exists.

        Example:

            http://localhost:8000/api/articles/?non_existent__exists=false
        """
        return self._field_filter_value(
            'non_existent_field__exists',
            'false',
            self.all_addresses_count
        )

    def test_field_filter_wildcard(self):
        """Test filter wildcard.

        Example:

            http://localhost:8000/api/articles/?title__wildcard=*elusional*
        """
        self._field_filter_value(
            'continent_country_city__wildcard',
            '*{}*'.format('ere'),  # Matches Yerevan
            self.addresses_in_yerevan_count
        )

        return self._field_filter_value(
            'continent_country_city__wildcard',
            '*{}*'.format('ire'),  # Matches Buenos Aires
            self.addresses_in_buenos_aires_count
        )

    def test_field_filter_exclude(self):
        """Test filter exclude.

        Example:

            http://localhost:8000/api/articles/?tags__exclude=children
        """
        return self._field_filter_value(
            'continent_country_city__exclude',
            'Yeovil',
            self.all_addresses_count - self.addresses_in_yeovil_count
        )

    # def test_field_filter_isnull_true(self):
    #     """Test filter isnull true.
    #
    #     Example:
    #
    #         http://localhost:8000/api/articles/?null_field__isnull=true
    #     """
    #     self._field_filter_value(
    #         'null_field__isnull',
    #         'true',
    #         self.all_count
    #     )
    #     self._field_filter_value(
    #         'tags__isnull',
    #         'true',
    #         self.no_tags_count
    #     )
    #
    # def test_field_filter_isnull_false(self):
    #     """Test filter isnull true.
    #
    #     Example:
    #
    #         http://localhost:8000/api/articles/?tags__isnull=false
    #     """
    #     self._field_filter_value(
    #         'null_field__isnull',
    #         'false',
    #         0
    #     )
    #     self._field_filter_value(
    #         'tags__isnull',
    #         'false',
    #         self.all_count - self.no_tags_count
    #     )

    def test_field_filter_endswith(self):
        """Test filter endswith.

        Example:

            http://localhost:8000/api/articles/?state__endswith=lished
        """
        self._field_filter_value(
            'continent_country_city__endswith',
            'dam',  # Matches Amsterdam
            self.addresses_in_amsterdam_count
        )
        return self._field_filter_value(
            'continent_country_city__endswith',
            'van',  # Matches Yerevan
            self.addresses_in_yerevan_count
        )

    def test_field_filter_contains(self):
        """Test filter contains.

        Example:

            http://localhost:8000/api/articles/?state__contains=lishe
        """
        self._field_filter_value(
            'continent_country_city__contains',
            'ster',  # Matches Amsterdam
            self.addresses_in_amsterdam_count
        )

        return self._field_filter_value(
            'continent_country_city__contains',
            'bli',  # Matches Dublin
            self.addresses_in_dublin_count
        )

    # def _field_filter_gte_lte(self, field_name, value, lookup, boost=None):
    #     """Field filter gt/gte/lt/lte.
    #
    #     Example:
    #
    #         http://localhost:8000/api/users/?id__gt=10
    #         http://localhost:8000/api/users/?id__gte=10
    #         http://localhost:8000/api/users/?id__lt=10
    #         http://localhost:8000/api/users/?id__lte=10
    #     """
    #     url = self.base_url[:]
    #     data = {}
    #
    #     if boost is not None:
    #         url += '?{}__{}={}|{}'.format(field_name, lookup, value, boost)
    #     else:
    #         url += '?{}__{}={}'.format(field_name, lookup, value)
    #
    #     response = self.client.get(
    #         url,
    #         data
    #     )
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #     __mapping = {
    #         'gt': self.assertGreater,
    #         'gte': self.assertGreaterEqual,
    #         'lt': self.assertLess,
    #         'lte': self.assertLessEqual,
    #     }
    #     __func = __mapping.get(lookup)
    #
    #     if callable(__func):
    #         for obj in response.data['results']:
    #             __func(
    #                 obj['id'],
    #                 value
    #             )
    #
    # def test_field_filter_gt(self):
    #     """Field filter gt.
    #
    #     Example:
    #
    #         http://localhost:8000/api/users/?id__gt=10
    #     :return:
    #     """
    #     return self._field_filter_gte_lte('id', self.in_progress[0].id, 'gt')
    #
    # def test_field_filter_gt_with_boost(self):
    #     """Field filter gt with boost.
    #
    #     Example:
    #
    #         http://localhost:8000/api/users/?id__gt=10|2.0
    #     :return:
    #     """
    #     # TODO: check boost value
    #     return self._field_filter_gte_lte(
    #         'id',
    #         self.in_progress[0].id,
    #         'gt',
    #         '2.0'
    #     )
    #
    # def test_field_filter_gte(self):
    #     """Field filter gte.
    #
    #     Example:
    #
    #         http://localhost:8000/api/users/?id__gte=10
    #     :return:
    #     """
    #     return self._field_filter_gte_lte(
    #         'id', self.in_progress[0].id, 'gte'
    #     )
    #
    # def test_field_filter_lt(self):
    #     """Field filter lt.
    #
    #     Example:
    #
    #         http://localhost:8000/api/users/?id__lt=10
    #     :return:
    #     """
    #     return self._field_filter_gte_lte('id', self.in_progress[0].id, 'lt')
    #
    # def test_field_filter_lt_with_boost(self):
    #     """Field filter lt with boost.
    #
    #     Example:
    #
    #         http://localhost:8000/api/users/?id__lt=10|2.0
    #     :return:
    #     """
    #     # TODO: check boost value
    #     return self._field_filter_gte_lte(
    #         'id',
    #         self.in_progress[0].id,
    #         'lt',
    #         '2.0'
    #     )
    #
    # def test_field_filter_lte(self):
    #     """Field filter lte.
    #
    #     Example:
    #
    #         http://localhost:8000/api/users/?id__lte=10
    #     :return:
    #     """
    #     return self._field_filter_gte_lte(
    #         'id', self.in_progress[0].id, 'lte'
    #     )
    #
    # def test_ids_filter(self):
    #     """Test ids filter.
    #
    #     Example:
    #
    #         http://localhost:8000/api/articles/?ids=68|64|58
    #         http://localhost:8000/api/articles/?ids=68&ids=64&ids=58
    #     """
    #     __ids = [str(__obj.id) for __obj in self.published]
    #     return self._field_filter_value(
    #         'ids',
    #         '|'.join(__ids),
    #         self.published_count
    #     )

    # ***********************************************************************
    # ******************** Core api and core schema *************************
    # ***********************************************************************

    @unittest.skipIf(not CORE_API_AND_CORE_SCHEMA_ARE_INSTALLED,
                     CORE_API_AND_CORE_SCHEMA_MISSING_MSG)
    def test_schema_fields_with_filter_fields_list(self):
        """Test schema field generator"""
        fields = self.backend.get_schema_fields(self.view)
        fields = [f.name for f in fields]
        self.assertEqual(fields, list(self.view.nested_filter_fields.keys()))

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
