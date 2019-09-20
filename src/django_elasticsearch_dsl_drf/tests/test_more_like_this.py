# coding: utf-8
"""
Test more-like-this functionality.
"""

from __future__ import absolute_import, unicode_literals

import unittest
import logging

from django.core.management import call_command

from nine.versions import DJANGO_GTE_1_10

import pytest

from rest_framework import status

import factories

from .base import BaseRestFrameworkTestCase

if DJANGO_GTE_1_10:
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

__title__ = 'django_elasticsearch_dsl_drf.tests.test_suggesters'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestMoreLikeThis',
)

LOGGER = logging.getLogger(__name__)


@pytest.mark.django_db
class TestMoreLikeThis(BaseRestFrameworkTestCase):
    """Test suggesters."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up class."""
        super(TestMoreLikeThis, cls).setUpClass()

        cls.lorem_books = factories.BookFactory.create_batch(200)

        cls.books = []

        cls.alice_books = []
        for book_data in factories.constants.NON_FAKER_BOOK_CONTENT:
            cls.alice_books.append(
                factories.BookChapterFactory(
                    title=book_data['title'],
                    summary=book_data['summary'],
                    description=book_data['description'],
                )
            )
        cls.alice_books_ids = [__obj.id for __obj in cls.alice_books]

        cls.sheckley_books = []
        for book_data in factories.constants.NON_FAKER_BOOK_CONTENT_OTHER:
            cls.sheckley_books.append(
                factories.BookNovelFactory(
                    title=book_data['title'],
                    summary=book_data['summary'],
                    description=book_data['description'],
                )
            )
        cls.sheckley_books_ids = [__obj.id for __obj in cls.sheckley_books]

        cls.books = []
        cls.books.extend(cls.alice_books)
        cls.books.extend(cls.sheckley_books)

        # Alice book
        cls.books_url_1 = reverse(
            'bookdocument_more_like_this-more-like-this',
            kwargs={'id': cls.books[0].id}
        )
        # Sheckley book
        cls.books_url_2 = reverse(
            'bookdocument_more_like_this-more-like-this',
            kwargs={'id': cls.books[-1].id}
        )

        # Alice book
        cls.books_url_1_no_options = reverse(
            'bookdocument_more_like_this_no_options-more-like-this',
            kwargs={'id': cls.books[0].id}
        )
        # Sheckley book
        cls.books_url_2_no_options = reverse(
            'bookdocument_more_like_this_no_options-more-like-this',
            kwargs={'id': cls.books[-1].id}
        )

        call_command('search_index', '--rebuild', '-f')

    def _test_more_like_this(self, test_data_ids, url, strict=True):
        """Test more-like-this.

        We can't really predict which result would it show as most relevant,
        however we can for sure assume that no strange data shall appear
        in between.
        """
        self.authenticate()
        data = {}
        response = self.client.get(
            url,
            data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if strict:
            response_ids = [int(__r['id']) for __r in response.data['results']]

            self.assertFalse(
                bool(
                    set(response_ids) - set(test_data_ids)
                )
            )

    def test_more_like_this(self):
        """Test more-like-this."""
        # Testing publishers
        test_data_ids = []
        test_data_ids.extend(self.alice_books_ids)
        test_data_ids.extend(self.sheckley_books_ids)

        self._test_more_like_this(
            test_data_ids,
            self.books_url_1,
            strict=True
        )
        self._test_more_like_this(
            test_data_ids,
            self.books_url_1_no_options,
            strict=False
        )

        self._test_more_like_this(
            test_data_ids,
            self.books_url_2,
            strict=True
        )
        self._test_more_like_this(
            test_data_ids,
            self.books_url_2_no_options,
            strict=False
        )


if __name__ == '__main__':
    unittest.main()
