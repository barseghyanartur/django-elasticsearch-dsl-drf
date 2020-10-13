from django.db import models

from six import python_2_unicode_compatible

__all__ = ('Publisher',)


@python_2_unicode_compatible
class Publisher(models.Model):
    """Publisher."""

    name = models.CharField(max_length=30)
    info = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()
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
    def location_shape_indexing(self):
        """
        Indexing point geo_shape.
        Used in Elasticsearch indexing/tests of `geo_shape` native filter.
        """
        return {
            'type': 'point',
            'coordinates': [self.latitude, self.longitude],
        }

    @property
    def location_circle_indexing(self):
        """
        Indexing circle geo_shape with 10km radius.
        Used in Elasticsearch indexing/tests of `geo_shape` native filter.
        """
        return {
            'type': 'circle',
            'coordinates': [self.latitude, self.longitude],
            'radius': '10km',
        }
