from django.contrib import admin

from .models import *

__all__ = (
    'AuthorAdmin',
    'BookAdmin',
    'OrderAdmin',
    'OrderLineAdmin',
    'PublisherAdmin',
    'TagAdmin',
)


@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    """Order line admin."""

    list_display = ('id', 'book',)
    search_fields = ('book__title',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order admin."""

    list_display = ('id', 'created', 'owner')
    filter_horizontal = ('lines',)
    # readonly_fields = ('lines',)
    fields = (
        'owner',
        'lines',
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Book admin."""

    list_display = ('title', 'isbn', 'price', 'publication_date')
    search_fields = ('title',)
    filter_horizontal = ('authors', 'tags',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Author admin."""

    list_display = ('name', 'email',)
    search_fields = ('name',)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """Publisher admin."""

    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin."""

    list_display = ('title',)
    search_fields = ('title',)
