from __future__ import unicode_literals

from django.db import models

from six import python_2_unicode_compatible

__all__ = ('Planet',)


@python_2_unicode_compatible
class Planet(models.Model):
    """Planet."""

    name = models.CharField(max_length=255)
    galaxy = models.ForeignKey('books.Galaxy', on_delete=models.CASCADE)

    class Meta(object):
        """Meta options."""

        ordering = ["id"]

    def __str__(self):
        return self.name
