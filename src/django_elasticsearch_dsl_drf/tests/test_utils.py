"""
Test utils.
"""

from __future__ import absolute_import

import unittest

from django.urls import reverse
from django.core.management import call_command

import pytest

from rest_framework import status

from .base import BaseRestFrameworkTestCase

__title__ = 'django_elasticsearch_dsl_drf.tests.test_utils'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestUtils',
)


@pytest.mark.django_db
class TestUtils(BaseRestFrameworkTestCase):
    """Test utils."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        super(TestUtils, cls).setUpClass()

        cls.sleep()
        call_command('search_index', '--rebuild', '-f')

    def _list_results(self):
        """List results."""
        self.authenticate()

        url = reverse('bookdocument_no_records-list', kwargs={})

        # Make request
        response = self.client.get(url, {})
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Should contain no results
        self.assertEqual(response.data['results'], [])
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['next'], None)
        self.assertEqual(response.data['previous'], None)

    def test_list_results(self):
        """Test list results."""
        return self._list_results()


if __name__ == '__main__':
    unittest.main()
