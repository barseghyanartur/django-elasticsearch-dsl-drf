from django.db import models

from six import python_2_unicode_compatible

from ..constants import (
    BOOK_PUBLISHING_STATUS_CHOICES,
    BOOK_PUBLISHING_STATUS_DEFAULT,
)

__all__ = ('Book',)


@python_2_unicode_compatible
class Book(models.Model):
    """Book."""

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    authors = models.ManyToManyField('books.Author', related_name='books')
    publisher = models.ForeignKey(
        'books.Publisher',
        related_name='books',
        on_delete=models.CASCADE
    )
    publication_date = models.DateField()
    state = models.CharField(
        max_length=100,
        choices=BOOK_PUBLISHING_STATUS_CHOICES,
        default=BOOK_PUBLISHING_STATUS_DEFAULT
    )
    isbn = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pages = models.PositiveIntegerField(default=200)
    stock_count = models.PositiveIntegerField(default=30)
    tags = models.ManyToManyField(
        'books.Tag',
        related_name='books',
        blank=True
    )

    class Meta(object):
        """Meta options."""

        ordering = ["isbn"]

    def __str__(self):
        return self.title

    @property
    def publisher_indexing(self):
        """Publisher for indexing.

        Used in Elasticsearch indexing.
        """
        if self.publisher is not None:
            return self.publisher.name

    @property
    def tags_indexing(self):
        """Tags for indexing.

        Used in Elasticsearch indexing.
        """
        return [tag.title for tag in self.tags.all()]

    @property
    def null_field_indexing(self):
        """null_field for indexing.

        Used in Elasticsearch indexing/tests of `isnull` functional filter.
        """
        return None
