# -*- coding: utf-8 -*-
"""
Test helpers.
"""

from __future__ import absolute_import, unicode_literals

import unittest

from django.core.management import call_command

import pytest

import factories

from ..helpers import more_like_this

from .base import BaseTestCase

__title__ = 'django_elasticsearch_dsl_drf.tests.test_helpers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
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
        super(TestHelpers, cls).setUpClass()
        cls.books_count = 30
        cls.books = []
        cls.books.append(
            factories.BookWithoutTagsFactory(
                title="Magic Of Thinking Big",
                description="Millions of people throughout the world have "
                            "improved their lives using The Magic of "
                            "Thinking Big. Dr. David J. Schwartz, long "
                            "regarded as one of the foremost experts on "
                            "motivation, will help you sell better, manage "
                            "better, earn more money, and-most important "
                            "of all-find greater happiness and peace of mind."
            )
        )
        cls.books.append(
            factories.BookWithoutTagsFactory(
                title="The Power of Positive Thinking",
                description="The book describes the power positive thinking "
                            "has and how a firm belief in something, does "
                            "actually help in achieving it."
            )
        )
        cls.books.append(
            factories.BookWithoutTagsFactory(
                title="Think and Grow Rich",
                description="Think And Grow Rich has earned itself the "
                            "reputation of being considered a textbook for "
                            "actionable techniques that can help one get "
                            "better at doing anything, not just by rich and "
                            "wealthy, but also by people doing wonderful work "
                            "in their respective fields."
            )
        )
        cls.books.append(
            factories.BookWithoutTagsFactory(
                title="The Magic of thinking Big",
                description="First published in 1959, David J Schwartz's "
                            "classic teachings are as powerful today as they "
                            "were then. Practical, empowering and hugely "
                            "engaging, this book will not only inspire you, "
                            "it will give you the tools to change your life "
                            "for the better - starting from now."
            )
        )
        cls.books.append(
            factories.BookWithoutTagsFactory(
                title="How to Stop Worrying and Start Living",
                description="The book is written to help readers by changing "
                            "their habit of worrying. The author Dale "
                            "Carnegie has shared his personal experiences, "
                            "wherein he was mostly unsatisfied and worried "
                            "about lot of life situations."
            )
        )
        cls.books.append(
            factories.BookWithoutTagsFactory(
                title="Practicing The Power Of Now",
                description="To make the journey into The Power of Now we "
                            "will need to leave our analytical mind and its "
                            "false created self, the ego, behind."
            )
        )

        cls.sleep()
        call_command('search_index', '--rebuild', '-f')

    def _more_like_this(self, obj, fields):
        """Filter by field."""
        res = more_like_this(obj, fields, 2, 2, 2, 10)
        self.assertGreater(res.count(), 0)

    def test_filter_by_field(self):
        """Filter by field."""
        obj = self.books[0]
        return self._more_like_this(obj, ['title', 'description'])


if __name__ == '__main__':
    unittest.main()
