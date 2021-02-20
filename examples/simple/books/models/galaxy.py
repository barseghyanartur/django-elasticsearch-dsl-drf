from __future__ import unicode_literals

from django.db import models

from six import python_2_unicode_compatible

__all__ = ('Galaxy',)


@python_2_unicode_compatible
class Galaxy(models.Model):
    """Galaxy."""

    name = models.CharField(max_length=255)

    class Meta(object):
        """Meta options."""

        ordering = ["id"]

    def __str__(self):
        return self.name
