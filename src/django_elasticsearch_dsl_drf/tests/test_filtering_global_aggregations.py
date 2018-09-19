"""
Test filtering `post_filter` backend.
"""

from __future__ import absolute_import

import unittest

from django.core.management import call_command

from nine.versions import DJANGO_GTE_1_10

import pytest

from rest_framework import status

from search_indexes.viewsets import BookDocumentViewSet

from ..filter_backends import PostFilterFilteringFilterBackend
from .base import BaseRestFrameworkTestCase
from .data_mixins import AddressesMixin, BooksMixin

if DJANGO_GTE_1_10:
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

__title__ = 'django_elasticsearch_dsl_drf.tests.test_filtering_post'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestFilteringGlobalAggregations',
)


@pytest.mark.django_db
class TestFilteringGlobalAggregations(BaseRestFrameworkTestCase,
                                      AddressesMixin,
                                      BooksMixin):
    """Test filtering with global aggregations."""

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

        # Testing coreapi and coreschema
        cls.backend = PostFilterFilteringFilterBackend()
        cls.view = BookDocumentViewSet()

    # ***********************************************************************
    # ************************ Test global facets ***************************
    # ***********************************************************************

    # This is what's it's all about - the facets.
    def _list_results_with_facets(self):
        """List results with facets."""
        self.authenticate()

        url = reverse('bookdocument-list', kwargs={})
        facet_state_url = url + '?facet=state_global'
        data = {}

        # ******************************************************************
        # ************************ No args response ************************
        # ******************************************************************

        # Make request
        no_args_response = self.client.get(url, data)
        self.assertEqual(no_args_response.status_code, status.HTTP_200_OK)

        # Should contain `self.all_count` results
        self.assertEqual(len(no_args_response.data['results']), self.all_count)

        # Should contain 1 facets
        self.assertEqual(len(no_args_response.data['facets']), 1)

        # ******************************************************************
        # ********************** With facets response **********************
        # ******************************************************************

        # Make request
        facet_state_response = self.client.get(facet_state_url, data)
        self.assertEqual(facet_state_response.status_code, status.HTTP_200_OK)

        # Should contain `self.all_count` results
        self.assertEqual(
            len(facet_state_response.data['results']), self.all_count
        )

        # Should contain 2 facets
        self.assertEqual(len(facet_state_response.data['facets']), 2)
        # With 3 statuses
        self.assertEqual(
            len(facet_state_response.data['facets']
                ['_filter_state_global']['state_global']['buckets']),
            3
        )

        self.assertIn(
            '_filter_state_global',
            facet_state_response.data['facets']
        )
        self.assertIn(
            'state_global',
            facet_state_response.data['facets']['_filter_state_global']
        )
        self.assertIn(
            'buckets',
            facet_state_response.data['facets']
                                     ['_filter_state_global']
                                     ['state_global']
        )
        # self.assertIn(
        #     'buckets',
        #     facet_state_response.data['facets']['_filter_state']['state']
        # )
        self.assertIn(
            {
                "doc_count": 10,
                "key": "published"
            },
            facet_state_response.data['facets']
                                     ['_filter_state_global']
                                     ['state_global']
                                     ['buckets']
        )
        self.assertIn(
            {
                "doc_count": 10,
                "key": "in_progress"
            },
            facet_state_response.data['facets']
            ['_filter_state_global']
            ['state_global']
            ['buckets']
        )
        self.assertIn(
            {
                "doc_count": 7,
                "key": "rejected"
            },
            facet_state_response.data['facets']
            ['_filter_state_global']
            ['state_global']
            ['buckets']
        )

        # ******************************************************************
        # ******************* With facets filtered response ****************
        # ******************************************************************

        facet_state_filtered_url = url + '?facet=state_global&state=published'
        # Make request
        facet_state_filtered_response = self.client.get(
            facet_state_filtered_url,
            data
        )
        self.assertEqual(
            facet_state_filtered_response.status_code,
            status.HTTP_200_OK
        )

        # Should contain `self.published_count` results
        self.assertEqual(
            len(facet_state_filtered_response.data['results']),
            self.published_count
        )

        # Should contain 2 facets
        self.assertEqual(len(facet_state_filtered_response.data['facets']), 2)
        # With 3 statuses
        self.assertEqual(
            len(facet_state_filtered_response.data['facets']
                ['_filter_state_global']['state_global']['buckets']),
            3
        )

        # Still same facets
        self.assertIn(
            {
                "doc_count": self.published_count,
                "key": "published"
            },
            facet_state_response.data['facets']
            ['_filter_state_global']
            ['state_global']
            ['buckets']
        )
        self.assertIn(
            {
                "doc_count": self.in_progress_count,
                "key": "in_progress"
            },
            facet_state_response.data['facets']
            ['_filter_state_global']
            ['state_global']
            ['buckets']
        )
        self.assertIn(
            {
                "doc_count": self.rejected_count,
                "key": "rejected"
            },
            facet_state_response.data['facets']
            ['_filter_state_global']
            ['state_global']
            ['buckets']
        )

    def test_list_results_with_facets(self):
        """Test list results with facets."""
        return self._list_results_with_facets()


if __name__ == '__main__':
    unittest.main()
