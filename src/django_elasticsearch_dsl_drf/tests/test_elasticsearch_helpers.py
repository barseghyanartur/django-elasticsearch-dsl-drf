# -*- coding: utf-8 -*-
"""
Test helpers.
"""

from __future__ import absolute_import, unicode_literals

import unittest

from django.core.management import call_command

import pytest

from ..elasticsearch_helpers import delete_all_indices, get_all_indices

from .base import BaseTestCase

__title__ = 'django_elasticsearch_dsl_drf.tests.test_elasticsearch_helpers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestElasticsearchHelpers',
)


@pytest.mark.django_db
class TestElasticsearchHelpers(BaseTestCase):
    """Test elasticsearch helpers."""

    pytestmark = pytest.mark.django_db

    def _get_all_indices(self):
        """Get all indices."""
        delete_all_indices(with_protected=True)

        self.sleep()
        call_command('search_index', '--rebuild', '-f')

        res = set(get_all_indices())
        expected = {
            'test_address',
            'test_location',
            'test_publisher',
            'test_journal',
            'test_city',
            'test_author',
            'test_book',
            'test_tag',
        }

        self.assertSetEqual(res, expected)

    def _delete_all_indices(self):
        """Delete all indices."""
        delete_all_indices(with_protected=True)

        res = get_all_indices()

        self.assertEqual(res, [])

    def test_all(self):
        """Filter by field."""
        self._get_all_indices()
        self._delete_all_indices()


if __name__ == '__main__':
    unittest.main()
