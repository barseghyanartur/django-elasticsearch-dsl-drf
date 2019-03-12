"""
Data mixins.
"""

from __future__ import absolute_import

import uuid

from nine.versions import DJANGO_GTE_1_10

from books import constants
import factories

if DJANGO_GTE_1_10:
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

__title__ = 'django_elasticsearch_dsl_drf.tests.data_mixins'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'AddressesMixin',
    'BooksMixin',
)


class AddressesMixin(object):
    """Addresses mixin."""

    @classmethod
    def created_addresses(cls):
        """Create addresses.

        :return:
        """

        # Testing nested objects: Addresses, cities and countries
        cls.addresses_in_yerevan_count = 16
        cls.addresses_in_yerevan = factories.AddressFactory.create_batch(
            cls.addresses_in_yerevan_count,
            **{
                'city__name': 'Yerevan',
                'city__country__name': 'Armenia',
                'city__country__continent__name': 'Europe',
            }
        )

        cls.addresses_in_amsterdam_count = 8
        cls.addresses_in_amsterdam = factories.AddressFactory.create_batch(
            cls.addresses_in_amsterdam_count,
            **{
                'city__name': 'Amsterdam',
                'city__country__name': 'Netherlands',
                'city__country__continent__name': 'Europe',
            }
        )

        # Some other addresses, cities and countries for correct counts
        # calculation.
        cls.addresses_in_dublin_count = 4
        cls.addresses_in_dublin = factories.AddressFactory.create_batch(
            cls.addresses_in_dublin_count,
            **{
                'city__name': 'Dublin',
                'city__country__name': 'Republic of Ireland',
                'city__country__continent__name': 'Europe',
            }
        )

        cls.addresses_in_yeovil_count = 2
        cls.addresses_in_yeovil = factories.AddressFactory.create_batch(
            cls.addresses_in_yeovil_count,
            **{
                'city__name': 'Yeovil',
                'city__country__name': 'United Kingdom',
                'city__country__continent__name': 'Europe',
            }
        )

        cls.addresses_in_buenos_aires_count = 1
        cls.addresses_in_buenos_aires = factories.AddressFactory.create_batch(
            cls.addresses_in_buenos_aires_count,
            **{
                'city__name': 'Buenos Aires',
                'city__country__name': 'Argentina',
                'city__country__continent__name': 'South America',
            }
        )

        cls.all_addresses_count = (
            cls.addresses_in_yerevan_count +
            cls.addresses_in_amsterdam_count +
            cls.addresses_in_dublin_count +
            cls.addresses_in_yeovil_count +
            cls.addresses_in_buenos_aires_count
        )

        cls.addresses_in_europe_count = (
            cls.addresses_in_yerevan_count +
            cls.addresses_in_amsterdam_count +
            cls.addresses_in_dublin_count +
            cls.addresses_in_yeovil_count
        )

        cls.addresses_in_south_america_count = \
            cls.addresses_in_buenos_aires_count

        cls.addresses_url = reverse('addressdocument-list', kwargs={})
        cls.addresses_suggest_url = reverse(
            'addressdocument-suggest',
            kwargs={}
        )

        city_id = cls.addresses_in_yerevan[0].city_id
        cls.cities_url = reverse('citydocument-list', kwargs={})
        cls.city_detail_url = reverse(
            'citydocument-detail', kwargs={'id': city_id}
        )


class BooksMixin(object):
    """Books mixin."""

    @classmethod
    def create_books(cls):
        """Create books.

        :return:
        """
        # Counts are primarily taken into consideration. Don't create Book
        # objects without `state`. If you don't know which state to use, use
        # ``constants.BOOK_PUBLISHING_STATUS_REJECTED``.
        cls.published_count = 10
        cls.published = factories.BookFactory.create_batch(
            cls.published_count,
            **{
                'state': constants.BOOK_PUBLISHING_STATUS_PUBLISHED,
            }
        )

        cls.in_progress_count = 10
        cls.in_progress = factories.BookFactory.create_batch(
            cls.in_progress_count,
            **{
                'state': constants.BOOK_PUBLISHING_STATUS_IN_PROGRESS,
            }
        )

        cls.prefix_count = 2
        cls.prefix = 'DelusionalInsanity'
        cls.prefixed = factories.BookFactory.create_batch(
            cls.prefix_count,
            **{

                'title': '{} {}'.format(cls.prefix, uuid.uuid4()),
                'state': constants.BOOK_PUBLISHING_STATUS_REJECTED,
            }
        )

        cls.no_tags_count = 5
        cls.no_tags = factories.BookWithoutTagsFactory.create_batch(
            cls.no_tags_count,
            **{
                'state': constants.BOOK_PUBLISHING_STATUS_REJECTED,
            }
        )

        cls.rejected_count = cls.prefix_count + cls.no_tags_count

        cls.all_count = (
            cls.published_count +
            cls.in_progress_count +
            cls.prefix_count +
            cls.no_tags_count
        )

        cls.base_url = reverse('bookdocument-list', kwargs={})
        cls.base_publisher_url = reverse('publisherdocument-list', kwargs={})
