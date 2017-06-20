from __future__ import absolute_import

import unittest

from django.core.management import call_command

import pytest

import factories

from ..helpers import more_like_this

from .base import BaseTestCase

__title__ = 'django_elasticsearch_dsl_drf.tests.test_filtering'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2016-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestHelpers',
)


@pytest.mark.django_db
class TestHelpers(BaseTestCase):
    """Test helpers."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        cls.published_count = 30
        cls.published = factories.BookWithUniqueTitleFactory.create_batch(
            cls.published_count
        )

        call_command('search_index', '--rebuild', '-f')

    def _more_like_this(self, obj, fields):
        """Filter by field."""
        res = more_like_this(obj, fields)
        self.assertGreater(res.count(), 0)

    def test_filter_by_field(self):
        """Filter by field."""
        obj = self.published[0]
        return self._more_like_this(obj, ['title', 'description'])


if __name__ == '__main__':
    unittest.main()
