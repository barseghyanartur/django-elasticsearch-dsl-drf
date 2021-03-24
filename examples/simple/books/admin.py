from django.contrib import admin

from .models import (
    Address,
    Author,
    Book,
    City,
    Continent,
    Country,
    Order,
    OrderLine,
    Publisher,
    Tag,
    Location,
)

__all__ = (
    'AddressAdmin',
    'AuthorAdmin',
    'BookAdmin',
    'CityAdmin',
    'ContinentAdmin',
    'CountryAdmin',
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

    list_display = ('id', 'title', 'isbn', 'price', 'publication_date')
    search_fields = ('title',)
    filter_horizontal = ('authors', 'tags',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Author admin."""

    list_display = ('id', 'name', 'email',)
    search_fields = ('name',)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """Publisher admin."""

    list_display = ('id', 'name', 'latitude', 'longitude',)
    list_editable = ('latitude', 'longitude',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin."""

    list_display = ('id', 'title',)
    search_fields = ('title',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Address admin."""

    list_display = ('id', 'street', 'house_number', 'zip_code', 'latitude',
                    'longitude', 'city',)
    list_editable = ('latitude', 'longitude',)
    search_fields = ('street',)
    list_filter = ('planet',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """City admin."""

    list_display = ('id', 'name', 'latitude', 'longitude',)
    list_editable = ('latitude', 'longitude',)
    search_fields = ('name',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Location admin."""

    list_display = (
        'id',
        'group',
        'latitude',
        'longitude',
        'address_street',
        'address_no',
        'postcode',
        'address_town',
    )
    search_fields = (
        'group',
        'postcode',
        'address_street',
        'address_town',
        'authority_name',
        'slug',
    )
    list_filter = ('occupation_status', 'group',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """Country admin."""

    list_display = ('id', 'name', 'latitude', 'longitude',)
    list_editable = ('latitude', 'longitude',)
    search_fields = ('name',)


@admin.register(Continent)
class ContinentAdmin(admin.ModelAdmin):
    """Continent admin."""

    list_display = ('id', 'name', 'latitude', 'longitude',)
    list_editable = ('latitude', 'longitude',)
    search_fields = ('name',)
