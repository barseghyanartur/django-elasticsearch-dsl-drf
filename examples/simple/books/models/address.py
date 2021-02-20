from __future__ import unicode_literals

from django.db import models
from django_elasticsearch_dsl_drf.wrappers import dict_to_obj

from six import python_2_unicode_compatible

__all__ = ('Address',)


@python_2_unicode_compatible
class Address(models.Model):
    """Address."""

    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=60)
    appendix = models.CharField(max_length=30, null=True, blank=True)
    zip_code = models.CharField(max_length=60)
    city = models.ForeignKey('books.City', on_delete=models.CASCADE)
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
    planet = models.ForeignKey('books.Planet', null=True, blank=True, on_delete=models.CASCADE)

    class Meta(object):
        """Meta options."""

        ordering = ["id"]

    def __str__(self):
        return "{} {} {} {}".format(
            self.street,
            self.house_number,
            self.appendix,
            self.zip_code
        )

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
    def country_indexing(self):
        """Country data (nested) for indexing.

        Example:

        >>> mapping = {
        >>>     'country': {
        >>>         'name': 'Netherlands',
        >>>         'city': {
        >>>             'name': 'Amsterdam',
        >>>         }
        >>>     }
        >>> }

        :return:
        """
        wrapper = dict_to_obj({
            'name': self.city.country.name,
            'city': {
                'name': self.city.name
            }
        })

        return wrapper

    @property
    def continent_indexing(self):
        """Continent data (nested) for indexing.

        Example:

        >>> mapping = {
        >>>     'continent': {
        >>>         'id': 2,
        >>>         'name': 'Asia',
        >>>         'country': {
        >>>             'id': 3,
        >>>             'name': 'Netherlands',
        >>>             'city': {
        >>>                 'id': 5,
        >>>                 'name': 'Amsterdam',
        >>>             }
        >>>         }
        >>>     }
        >>> }

        :return:
        """
        wrapper = dict_to_obj({
            'id': self.city.country.continent.id,
            'name': self.city.country.continent.name,
            'country': {
                'id': self.city.country.id,
                'name': self.city.country.name,
                'city': {
                    'id': self.city.id,
                    'name': self.city.name,
                }
            }
        })

        return wrapper

    @property
    def galaxy_indexing(self):
        """Galaxy data (nested) for indexing.

        Example:

        >>> mapping = {
        >>>     'galaxy': {
        >>>         'id': 2,
        >>>         'name': 'Milky Way',
        >>>         'planet': {
        >>>             'id': 3,
        >>>             'name': 'Earth',
        >>>         }
        >>>     }
        >>> }

        :return:
        """
        wrapper = dict_to_obj({
            'id': self.planet.galaxy.id,
            'name': self.planet.galaxy.name,
            'planet': {
                'id': self.planet.id,
                'name': self.planet.name,
            }
        })

        return wrapper
