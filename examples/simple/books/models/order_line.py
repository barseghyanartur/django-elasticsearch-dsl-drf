from __future__ import unicode_literals

from django.db import models

__all__ = ('OrderLine',)


class OrderLine(models.Model):
    """Order line."""

    book = models.ForeignKey(
        'books.Book',
        related_name='order_lines',
        on_delete=models.CASCADE
    )

    class Meta:
        """Meta options."""

        ordering = ["order__created"]

    def __str__(self):
        return '{}'.format(self.book.isbn)
