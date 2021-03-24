from __future__ import unicode_literals

from django.db import models

__all__ = ('Planet',)


class Planet(models.Model):
    """Planet."""

    name = models.CharField(max_length=255)
    galaxy = models.ForeignKey('books.Galaxy', on_delete=models.CASCADE)

    class Meta:
        """Meta options."""

        ordering = ["id"]

    def __str__(self):
        return self.name
