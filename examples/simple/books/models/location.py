from django.db import models

from six import python_2_unicode_compatible

from ..constants import (
    YES,
    NO,
    LOCATION_CATEGORY_CHOICES
)

__all__ = ('Location',)


@python_2_unicode_compatible
class Location(models.Model):
    """Location."""

    group = models.CharField(max_length=255, choices=LOCATION_CATEGORY_CHOICES)
    occupation_status = models.BooleanField()
    postcode = models.CharField(max_length=50)
    address_no = models.CharField(max_length=255)
    address_street = models.CharField(max_length=255)
    address_town = models.CharField(max_length=255)
    authority_name = models.CharField(max_length=255)
    # geocode = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    floor_area = models.FloatField()
    employee_count = models.FloatField()
    rental_valuation = models.FloatField()
    revenue = models.FloatField()
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
        return self.full

    @property
    def geocode(self):
        return self.postcode

    @property
    def occupation_status_text(self):
        """Publisher for indexing.

        Used in Elasticsearch indexing.
        """
        return YES if self.occupation_status else NO

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
    def full(self):
        return "{address_street} {address_no}, {postcode} {address_town}" \
               "{authority_name}".format(
                    address_street=self.address_street,
                    address_no=self.address_no,
                    postcode=self.postcode,
                    address_town=self.address_town,
                    authority_name=self.authority_name
                )

    @property
    def partial(self):
        return self.address_town
