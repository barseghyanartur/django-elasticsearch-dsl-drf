from django.conf import settings
from django.db import models

__all__ = ('Journal',)


class Journal(models.Model):
    """Journal."""

    isbn = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pages = models.PositiveIntegerField(default=200)
    stock_count = models.PositiveIntegerField(default=30)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        """Meta options."""

        ordering = ["isbn"]

    def __str__(self):
        return self.title

    @property
    def created_indexing(self):
        return self.created.strftime(settings.ELASTICSEARCH_DATETIME_FORMAT)
