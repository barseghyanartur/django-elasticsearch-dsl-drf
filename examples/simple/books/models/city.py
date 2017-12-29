from __future__ import unicode_literals

import datetime

from django.db import models

from six import python_2_unicode_compatible

__all__ = ('City',)


@python_2_unicode_compatible
class City(models.Model):
    """City."""

    name = models.CharField(max_length=255)
    info = models.TextField(null=True, blank=True)
    country = models.ForeignKey('books.Country', on_delete=models.CASCADE)
    latitude = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=15,
        max_digits=19,
        default=0
    )
    longitude = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=15,
        max_digits=19,
        default=0
    )

    class Meta(object):
        """Meta options."""

        ordering = ["id"]

    def __str__(self):
        return self.name

    @property
    def location_field_indexing(self):
        """Location for indexing.

        Used in Elasticsearch indexing/tests of `geo_distance` native filter.
        """
        return {
            'lat': self.latitude,
            'lon': self.longitude,
        }

    @property
    def boolean_list_indexing(self):
        """Boolean list for indexing.

        Used in Elasticsearch indexing/tests of complex fields.
        """
        return [True, False]

    @property
    def boolean_dict_indexing(self):
        """Boolean dict for indexing.

        Used in Elasticsearch indexing/tests of complex fields.
        """
        return {'true': True, 'false': False}

    @property
    def datetime_list_indexing(self):
        """Date list for indexing.

        Used in Elasticsearch indexing/tests of complex fields.
        """
        return [
            datetime.datetime.now(),
            datetime.datetime.now() - datetime.timedelta(days=1)
        ]

    @property
    def datetime_dict_indexing(self):
        """Date dict for indexing.

        Used in Elasticsearch indexing/tests of complex fields.
        """
        return {
            'today': datetime.datetime.now(),
            'yesterday': datetime.datetime.now() - datetime.timedelta(days=1)
        }

    @property
    def float_list_indexing(self):
        """Float list for indexing.

        Used in Elasticsearch indexing/tests of complex fields.
        """
        return [3.14159, 2.71828]

    @property
    def float_dict_indexing(self):
        """Float dict for indexing.

        Used in Elasticsearch indexing/tests of complex fields.
        """
        return {'pi': 3.14159, 'e': 2.71828}

    @property
    def integer_list_indexing(self):
        """Integer list for indexing.

        Used in Elasticsearch indexing/tests of complex fields.
        """
        return [12, 5]

    @property
    def integer_dict_indexing(self):
        """Integer dict for indexing.

        Used in Elasticsearch indexing/tests of complex fields.
        """
        return {'twelve': 12, 'five': 5}
