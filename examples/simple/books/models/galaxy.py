from __future__ import unicode_literals

from django.db import models

__all__ = ('Galaxy',)


class Galaxy(models.Model):
    """Galaxy."""

    name = models.CharField(max_length=255)

    class Meta:
        """Meta options."""

        ordering = ["id"]

    def __str__(self):
        return self.name
