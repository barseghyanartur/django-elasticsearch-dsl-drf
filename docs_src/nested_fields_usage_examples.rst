============================
Nested fields usage examples
============================

Advanced Django REST framework integration examples with object/nested fields.

See the `example project
<https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/tree/master/examples/simple>`_
for sample models/views/serializers.

- `models
  <https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/blob/master/examples/simple/books/__init__.py>`_
- `documents
  <https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/blob/master/examples/simple/search_indexes/documents/__init__.py>`_
- `serializers
  <https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/blob/master/examples/simple/search_indexes/serializers/__init__.py>`_
- `viewsets
  <https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/blob/master/examples/simple/search_indexes/viewsets/__init__.py>`_

Contents:

.. contents:: Table of Contents

Example app
===========

Sample models
-------------

*books/models/continent.py*

.. code-block:: python

    from django.db import models

    from six import python_2_unicode_compatible

    @python_2_unicode_compatible
    class Continent(models.Model):
        """Continent."""

        name = models.CharField(max_length=255)
        info = models.TextField(null=True, blank=True)
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

*books/models/country.py*

.. code-block:: python

    @python_2_unicode_compatible
    class Country(models.Model):
        """Country."""

        name = models.CharField(max_length=255)
        info = models.TextField(null=True, blank=True)
        continent = models.ForeignKey(
            'books.Continent',
            on_delete=models.CASCADE
        )
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

            Used in Elasticsearch indexing/tests of `geo_distance` native
            filter.
            """
            return {
                'lat': self.latitude,
                'lon': self.longitude,
            }


*books/models/city.py*

.. code-block:: python

    @python_2_unicode_compatible
    class City(models.Model):
        """City."""

        name = models.CharField(max_length=255)
        info = models.TextField(null=True, blank=True)
        country = models.ForeignKey('books.Country', on_delete=models.CASCADE)
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

            Used in Elasticsearch indexing/tests of `geo_distance` native
            filter.
            """
            return {
                'lat': self.latitude,
                'lon': self.longitude,
            }

*books/models/address.py*

.. code-block:: python

    from django.db import models
    from django_elasticsearch_dsl_drf.wrappers import dict_to_obj

    from six import python_2_unicode_compatible

    @python_2_unicode_compatible
    class Address(models.Model):
        """Address."""

        street = models.CharField(max_length=255)
        house_number = models.CharField(max_length=60)
        appendix = models.CharField(max_length=30, null=True, blank=True)
        zip_code = models.CharField(max_length=60)
        city = models.ForeignKey('books.City', on_delete=models.CASCADE)
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
            return "{} {} {} {}".format(
                self.street,
                self.house_number,
                self.appendix,
                self.zip_code
            )

        @property
        def location_field_indexing(self):
            """Location for indexing.

            Used in Elasticsearch indexing/tests of `geo_distance` native
            filter.
            """
            return {
                'lat': self.latitude,
                'lon': self.longitude,
            }

        @property
        def country_indexing(self):
            """Country data (nested) for indexing.

            Example:

            >>> mapping = {
            >>>     'country': {
            >>>         'name': 'Netherlands',
            >>>         'city': {
            >>>             'name': 'Amsterdam',
            >>>         }
            >>>     }
            >>> }

            :return:
            """
            wrapper = dict_to_obj({
                'name': self.city.country.name,
                'city': {
                    'name': self.city.name
                }
            })

            return wrapper

        @property
        def continent_indexing(self):
            """Continent data (nested) for indexing.

            Example:

            >>> mapping = {
            >>>     'continent': {
            >>>         'name': 'Asia',
            >>>         'country': {
            >>>             'name': 'Netherlands',
            >>>             'city': {
            >>>                 'name': 'Amsterdam',
            >>>             }
            >>>         }
            >>>     }
            >>> }

            :return:
            """
            wrapper = dict_to_obj({
                'name': self.city.country.continent.name,
                'country': {
                    'name': self.city.country.name,
                    'city': {
                        'name': self.city.name,
                    }
                }
            })

            return wrapper

Sample document
---------------

Index definition
~~~~~~~~~~~~~~~~

To separate dev/test/staging/production indexes, the following approach is
recommended.

Settings
^^^^^^^^

*settings/base.py*

.. code-block:: python

    # Name of the Elasticsearch index
    ELASTICSEARCH_INDEX_NAMES = {
        'search_indexes.documents.address': 'address',
    }

*settings/testing.py*

.. code-block:: python

    # Name of the Elasticsearch index
    ELASTICSEARCH_INDEX_NAMES = {
        'search_indexes.documents.address': 'test_address',
    }

*settings/production.py*

.. code-block:: python

    # Name of the Elasticsearch index
    ELASTICSEARCH_INDEX_NAMES = {
        'search_indexes.documents.address': 'prod_address',
    }

Document index
^^^^^^^^^^^^^^

*search_indexes/documents/address.py*

.. code-block:: python

    from django.conf import settings

    from django_elasticsearch_dsl import DocType, Index, fields
    from django_elasticsearch_dsl_drf.compat import KeywordField, StringField

    from books.models import Address

    from .analyzers import html_strip


    INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

    # See Elasticsearch Indices API reference for available settings
    INDEX.settings(
        number_of_shards=1,
        number_of_replicas=1
    )

    @INDEX.doc_type
    class AddressDocument(DocType):
        """Address Elasticsearch document."""

        # In different parts of the code different fields are used. There are
        # a couple of use cases: (1) more-like-this functionality, where `title`,
        # `description` and `summary` fields are used, (2) search and filtering
        # functionality where all of the fields are used.

        # ID
        id = fields.IntegerField(attr='id')

        # ********************************************************************
        # *********************** Main data fields for search ****************
        # ********************************************************************

        street = StringField(
            analyzer=html_strip,
            fields={
                'raw': KeywordField(),
                'suggest': fields.CompletionField(),
            }
        )

        house_number = StringField(analyzer=html_strip)

        appendix = StringField(analyzer=html_strip)

        zip_code = StringField(
            analyzer=html_strip,
            fields={
                'raw': KeywordField(),
                'suggest': fields.CompletionField(),
            }
        )

        # ********************************************************************
        # ********** Additional fields for search and filtering **************
        # ********************************************************************

        # City object
        city = fields.ObjectField(
            properties={
                'name': StringField(
                    analyzer=html_strip,
                    fields={
                        'raw': KeywordField(),
                        'suggest': fields.CompletionField(),
                    }
                ),
                'info': StringField(analyzer=html_strip),
                'location': fields.GeoPointField(attr='location_field_indexing'),
                'country': fields.ObjectField(
                    properties={
                        'name': StringField(
                            analyzer=html_strip,
                            fields={
                                'raw': KeywordField(),
                                'suggest': fields.CompletionField(),
                            }
                        ),
                        'info': StringField(analyzer=html_strip),
                        'location': fields.GeoPointField(
                            attr='location_field_indexing'
                        )
                    }
                )
            }
        )

        # Country object
        country = fields.NestedField(
            attr='country_indexing',
            properties={
                'name': StringField(
                    analyzer=html_strip,
                    fields={
                        'raw': KeywordField(),
                        'suggest': fields.CompletionField(),
                    }
                ),
                'city': fields.ObjectField(
                    properties={
                        'name': StringField(
                            analyzer=html_strip,
                            fields={
                                'raw': KeywordField(),
                            },
                        ),
                    },
                ),
            },
        )

        # Continent object
        continent = fields.NestedField(
            attr='continent_indexing',
            properties={
                'name': StringField(
                    analyzer=html_strip,
                    fields={
                        'raw': KeywordField(),
                        'suggest': fields.CompletionField(),
                    }
                ),
                'country': fields.NestedField(
                    properties={
                        'name': StringField(
                            analyzer=html_strip,
                            fields={
                                'raw': KeywordField(),
                            }
                        ),
                        'city': fields.NestedField(
                            properties={
                                'name': StringField(
                                    analyzer=html_strip,
                                    fields={
                                        'raw': KeywordField(),
                                    }
                                )
                            }
                        )
                    }
                )
            }
        )

        location = fields.GeoPointField(attr='location_field_indexing')

        class Meta(object):
            """Meta options."""

            model = Address  # The model associate with this DocType

Sample serializer
-----------------

*search_indexes/serializers/address.py*

.. code-block:: python

    from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

    from ..documents import AddressDocument


    class AddressDocumentSerializer(DocumentSerializer):
        """Serializer for address document."""

        class Meta(object):
            """Meta options."""

            document = AddressDocument
            fields = (
                'id',
                'street',
                'house_number',
                'appendix',
                'zip_code',
                'city',
                'country',
                'continent',
                'location',
            )


Sample view
-----------

*search_indexes/viewsets/address.py*

.. code-block:: python

    from django_elasticsearch_dsl_drf.constants import (
        LOOKUP_FILTER_GEO_DISTANCE,
        LOOKUP_FILTER_GEO_POLYGON,
        LOOKUP_FILTER_GEO_BOUNDING_BOX,
        SUGGESTER_COMPLETION,
    )
    from django_elasticsearch_dsl_drf.filter_backends import (
        DefaultOrderingFilterBackend,
        FacetedSearchFilterBackend,
        FilteringFilterBackend,
        GeoSpatialFilteringFilterBackend,
        GeoSpatialOrderingFilterBackend,
        NestedFilteringFilterBackend,
        OrderingFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend,
    )
    from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
    from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

    from ..documents import AddressDocument
    from ..serializers import AddressDocumentSerializer

    class AddressDocumentViewSet(DocumentViewSet):
        """The AddressDocument view."""

        document = AddressDocument
        serializer_class = AddressDocumentSerializer
        lookup_field = 'id'
        filter_backends = [
            FacetedSearchFilterBackend,
            FilteringFilterBackend,
            OrderingFilterBackend,
            SearchFilterBackend,
            GeoSpatialFilteringFilterBackend,
            GeoSpatialOrderingFilterBackend,
            NestedFilteringFilterBackend,
            DefaultOrderingFilterBackend,
            SuggesterFilterBackend,
        ]
        pagination_class = LimitOffsetPagination
        # Define search fields
        search_fields = (
            'street',
            'zip_code',
            'city.name',
            'city.country.name',
        )
        # Define filtering fields
        filter_fields = {
            'id': None,
            'city': 'city.name.raw',
        }
        # Nested filtering fields
        nested_filter_fields = {
            'continent_country': {
                'field': 'continent.country.name.raw',
                'path': 'continent.country',
            },
            'continent_country_city': {
                'field': 'continent.country.city.name.raw',
                'path': 'continent.country.city',
            },
        }
        # Define geo-spatial filtering fields
        geo_spatial_filter_fields = {
            'location': {
                'lookups': [
                    LOOKUP_FILTER_GEO_BOUNDING_BOX,
                    LOOKUP_FILTER_GEO_DISTANCE,
                    LOOKUP_FILTER_GEO_POLYGON,

                ],
            },
        }
        # Define ordering fields
        ordering_fields = {
            'id': None,
            'street': None,
            'city': 'city.name.raw',
            'country': 'city.country.name.raw',
            'zip_code': None,
        }
        # Define ordering fields
        geo_spatial_ordering_fields = {
            'location': None,
        }
        # Specify default ordering
        ordering = (
            'id',
            'street.raw',
            'city.name.raw',
        )
        # Suggester fields
        suggester_fields = {
            'street_suggest': {
                'field': 'street.suggest',
                'suggesters': [
                    SUGGESTER_COMPLETION,
                ],
            },
            'city_suggest': {
                'field': 'city.name.suggest',
                'suggesters': [
                    SUGGESTER_COMPLETION,
                ],
            },
            'country_suggest': {
                'field': 'city.country.name.suggest',
                'suggesters': [
                    SUGGESTER_COMPLETION,
                ],
            }
        }

        # Facets
        faceted_search_fields = {
            'city': {
                'field': 'city.name.raw',
                'enabled': True,
            },
            'country': {
                'field': 'city.country.name.raw',
                'enabled': True,
            },
        }

Usage example
-------------
Considering samples above, you should be able to perform the search, sorting
and filtering actions described below.

Sample queries
~~~~~~~~~~~~~~

Search
^^^^^^
Just a couple of examples, because searching in nested fields doesn't differ
from searching in simple fields.

**Search in all fields**

Search in all fields (``street``, ``zip_code`` and ``city``, ``country``) for
word "Picadilly".

.. code-block:: text

    http://127.0.0.1:8000/search/addresses/?search=Piccadilly

**Search a single term on specific field**

In order to search in specific field (``country``) for term "Armenia", add
the field name separated with ``|`` to the search term.

.. code-block:: text

    http://127.0.0.1:8000/search/addresses/?search=city.country.name:Armenia

Nested filtering
^^^^^^^^^^^^^^^^

**Filter documents by nested field**

Filter documents by field (``continent.country``) "Armenia".

.. code-block:: text

    http://127.0.0.1:8000/search/addresses/?continent_country=Armenia

Filter documents by field (``continent.country.city``) "Amsterdam".

.. code-block:: text

    http://127.0.0.1:8000/search/addresses/?continent_country_city=Amsterdam

Nested search
^^^^^^^^^^^^^
For nested search, let's have another example.

Sample models
+++++++++++++

*books/models/city.py*

.. code-block:: python

    from django.db import models
    from six import python_2_unicode_compatible

    @python_2_unicode_compatible
    class City(models.Model):
        """City."""

        name = models.CharField(max_length=255)
        info = models.TextField(null=True, blank=True)
        country = models.ForeignKey('books.Country')
        latitude = models.DecimalField(null=True,
                                       blank=True,
                                       decimal_places=15,
                                       max_digits=19,
                                       default=0)
        longitude = models.DecimalField(null=True,
                                        blank=True,
                                        decimal_places=15,
                                        max_digits=19,
                                        default=0)

*books/models/country.py*

.. code-block:: python

    from django.db import models
    from six import python_2_unicode_compatible

    @python_2_unicode_compatible
    class Country(models.Model):
        """Country."""

        name = models.CharField(max_length=255)
        info = models.TextField(null=True, blank=True)
        latitude = models.DecimalField(null=True,
                                       blank=True,
                                       decimal_places=15,
                                       max_digits=19,
                                       default=0)
        longitude = models.DecimalField(null=True,
                                        blank=True,
                                        decimal_places=15,
                                        max_digits=19,
                                        default=0)

Sample document
+++++++++++++++

*documents/city.py*

.. code-block:: python

    from django.conf import settings

    from django_elasticsearch_dsl import DocType, Index, fields
    from django_elasticsearch_dsl_drf.compat import KeywordField, StringField

    from books.models import City

    from .analyzers import html_strip

    INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

    # See Elasticsearch Indices API reference for available settings
    INDEX.settings(
        number_of_shards=1,
        number_of_replicas=1
    )


    @INDEX.doc_type
    class CityDocument(DocType):
        """City Elasticsearch document.

        This document has been created purely for testing out complex fields.
        """

        # ID
        id = fields.IntegerField(attr='id')

        # ********************************************************************
        # ********************** Main data fields for search *****************
        # ********************************************************************

        name = StringField(
            analyzer=html_strip,
            fields={
                'raw': KeywordField(),
                'suggest': fields.CompletionField(),
            }
        )

        info = StringField(analyzer=html_strip)

        # ********************************************************************
        # ************** Nested fields for search and filtering **************
        # ********************************************************************

        # City object
        country = fields.NestedField(
            properties={
                'name': StringField(
                    analyzer=html_strip,
                    fields={
                        'raw': KeywordField(),
                        'suggest': fields.CompletionField(),
                    }
                ),
                'info': StringField(analyzer=html_strip),
                'location': fields.GeoPointField(attr='location_field_indexing'),
            }
        )

        location = fields.GeoPointField(attr='location_field_indexing')

        # ********************************************************************
        # ********** Other complex fields for search and filtering ***********
        # ********************************************************************

        boolean_list = fields.ListField(
            StringField(attr='boolean_list_indexing')
        )

        datetime_list = fields.ListField(
            StringField(attr='datetime_list_indexing')
        )
        float_list = fields.ListField(
            StringField(attr='float_list_indexing')
        )
        integer_list = fields.ListField(
            StringField(attr='integer_list_indexing')
        )

        class Meta(object):
            """Meta options."""

            model = City  # The model associate with this DocType

Sample view
+++++++++++

*viewsets/city.py*

.. code-block:: python

    from django_elasticsearch_dsl_drf.constants import (
        LOOKUP_FILTER_GEO_DISTANCE,
        LOOKUP_FILTER_GEO_POLYGON,
        LOOKUP_FILTER_GEO_BOUNDING_BOX,
        SUGGESTER_COMPLETION,
    )
    from django_elasticsearch_dsl_drf.filter_backends import (
        FilteringFilterBackend,
        DefaultOrderingFilterBackend,
        OrderingFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend,
        GeoSpatialFilteringFilterBackend,
        GeoSpatialOrderingFilterBackend,
    )
    from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
    from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

    from ..documents import CityDocument
    from ..serializers import CityDocumentSerializer

    class CityDocumentViewSet(BaseDocumentViewSet):
        """The CityDocument view."""

        document = CityDocument
        serializer_class = CityDocumentSerializer
        lookup_field = 'id'
        filter_backends = [
            FilteringFilterBackend,
            OrderingFilterBackend,
            SearchFilterBackend,
            GeoSpatialFilteringFilterBackend,
            GeoSpatialOrderingFilterBackend,
            DefaultOrderingFilterBackend,
            SuggesterFilterBackend,
        ]
        pagination_class = LimitOffsetPagination
        # Define search fields
        search_fields = (
            'name',
            'info',
        )

        search_nested_fields = {
            'country': {
                'path': 'country',
                'fields': ['name'],
            }
        }

        # Define filtering fields
        filter_fields = {
            'id': None,
            'name': 'name.raw',
            'country': 'country.name.raw',
        }
        # Define geo-spatial filtering fields
        geo_spatial_filter_fields = {
            'location': {
                'lookups': [
                    LOOKUP_FILTER_GEO_BOUNDING_BOX,
                    LOOKUP_FILTER_GEO_DISTANCE,
                    LOOKUP_FILTER_GEO_POLYGON,

                ],
            },
        }
        # Define ordering fields
        ordering_fields = {
            'id': None,
            'name': None,
            'country': 'country.name.raw',
        }
        # Define ordering fields
        geo_spatial_ordering_fields = {
            'location': None,
        }
        # Specify default ordering
        ordering = (
            'id',
            'name.raw',
            'country.name.raw',
        )

        # Suggester fields
        suggester_fields = {
            'name_suggest': {
                'field': 'name.suggest',
                'suggesters': [
                    SUGGESTER_COMPLETION,
                ],
            },
            'country_suggest': {
                'field': 'country.name.suggest',
                'suggesters': [
                    SUGGESTER_COMPLETION,
                ],
            }
        }


Sample request
++++++++++++++

**Request**

.. code-block:: text

    GET http://127.0.0.1:8000/search/cities/?search=Switzerland

Filtering
^^^^^^^^^

**Filter documents by field**

Filter documents by field (``city``) "Dublin".

.. code-block:: text

    http://127.0.0.1:8000/search/addresses/?city=Dublin

**Filter documents by multiple fields**

Filter documents by field (``states``) "published" and "in_progress".

.. code-block:: text

    http://127.0.0.1:8000/search/addresses/?city__in=Yerevan__Dublin

Ordering
^^^^^^^^

The ``-`` prefix means ordering should be descending.

**Order documents by field (descending)**

Order documents by field ``country`` (ascending).

.. code-block:: text

    http://127.0.0.1:8000/search/addresses/?ordering=-country

Suggestions
-----------

The suggest feature suggests similar looking terms based on a provided text
by using a suggester.

.. note::

    The ``SuggesterFilterBackend`` filter backend can be used in the
    ``suggest`` custom view action/route only. Usages outside of the are
    ``suggest`` action/route are restricted.

There are three options available here: ``term``, ``phrase`` and
``completion``.

.. note::

    Suggestion functionality is exclusive. Once you have queried the
    ``SuggesterFilterBackend``, the latter will transform your current
    search query into suggestion search query (which is very different).
    Therefore, always add it as the very last filter backend.

Suggest completion for field ``country``.

.. code-block:: text

    http://127.0.0.1:8000/search/addresses/suggest/?country_suggest__completion=Ar


Suggest completion for field ``city``.

.. code-block:: text

    http://127.0.0.1:8000/search/addresses/suggest/?city_suggest__completion=Ye

Nested aggregations/facets
--------------------------
At the moment, nested aggregations/facets are not supported out of the box.
Out of the box support will surely land in the package one day, but for now,
there's a simple and convenient way of implementing nested aggregations/facets
with minimal efforts. Consider the following example.

*search_indexes/backends/nested_continents.py*

.. code-block:: python

    from django_elasticsearch_dsl_drf.filter_backends.mixins import (
        FilterBackendMixin,
    )
    from rest_framework.filters import BaseFilterBackend

    class NestedContinentsBackend(BaseFilterBackend, FilterBackendMixin):
        """Adds nesting to continents."""

        faceted_search_param = 'nested_facet'

        def get_faceted_search_query_params(self, request):
            """Get faceted search query params.

            :param request: Django REST framework request.
            :type request: rest_framework.request.Request
            :return: List of search query params.
            :rtype: list
            """
            query_params = request.query_params.copy()
            return query_params.getlist(self.faceted_search_param, [])

        def filter_queryset(self, request, queryset, view):
            """Filter the queryset.
            :param request: Django REST framework request.
            :param queryset: Base queryset.
            :param view: View.
            :type request: rest_framework.request.Request
            :type queryset: elasticsearch_dsl.search.Search
            :type view: rest_framework.viewsets.ReadOnlyModelViewSet
            :return: Updated queryset.
            :rtype: elasticsearch_dsl.search.Search
            """
            facets = self.get_faceted_search_query_params(request)

            if 'continent' in facets:
                queryset \
                    .aggs\
                    .bucket('continents',
                            'nested',
                            path='continent') \
                    .bucket('continent_name',
                            'terms',
                            field='continent.name.raw',
                            size=10) \
                    .bucket('counties',
                            'nested',
                            path='continent.country') \
                    .bucket('country_name',
                            'terms',
                            field='continent.country.name.raw',
                            size=10) \
                    .bucket('city',
                            'nested',
                            path='continent.country.city') \
                    .bucket('city_name',
                            'terms',
                            field='continent.country.city.name.raw',
                            size=10)

            return queryset

The view will look as follows:

*search_indexes/viewsets/address.py*

.. code-block:: python

    from django_elasticsearch_dsl_drf.constants import (
        LOOKUP_FILTER_GEO_DISTANCE,
        LOOKUP_FILTER_GEO_POLYGON,
        LOOKUP_FILTER_GEO_BOUNDING_BOX,
        SUGGESTER_COMPLETION,
    )
    from django_elasticsearch_dsl_drf.filter_backends import (
        DefaultOrderingFilterBackend,
        FacetedSearchFilterBackend,
        FilteringFilterBackend,
        GeoSpatialFilteringFilterBackend,
        GeoSpatialOrderingFilterBackend,
        NestedFilteringFilterBackend,
        OrderingFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend,
    )
    from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
    from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

    from ..backends import NestedContinentsBackend
    from ..documents import AddressDocument
    from ..serializers import AddressDocumentSerializer

    class AddressDocumentViewSet(DocumentViewSet):
        """The AddressDocument view."""

        document = AddressDocument
        serializer_class = AddressDocumentSerializer
        lookup_field = 'id'
        filter_backends = [
            FacetedSearchFilterBackend,
            FilteringFilterBackend,
            OrderingFilterBackend,
            SearchFilterBackend,
            GeoSpatialFilteringFilterBackend,
            GeoSpatialOrderingFilterBackend,
            NestedContinentsBackend,
            NestedFilteringFilterBackend,
            DefaultOrderingFilterBackend,
            SuggesterFilterBackend,
        ]
        pagination_class = LimitOffsetPagination
        # Define search fields
        search_fields = (
            'street',
            'zip_code',
            'city.name',
            'city.country.name',
        )
        # Define filtering fields
        filter_fields = {
            'id': None,
            'city': 'city.name.raw',
        }
        # Nested filtering fields
        nested_filter_fields = {
            'continent_country': {
                'field': 'continent.country.name.raw',
                'path': 'continent.country',
            },
            'continent_country_city': {
                'field': 'continent.country.city.name.raw',
                'path': 'continent.country.city',
            },
        }
        # Define geo-spatial filtering fields
        geo_spatial_filter_fields = {
            'location': {
                'lookups': [
                    LOOKUP_FILTER_GEO_BOUNDING_BOX,
                    LOOKUP_FILTER_GEO_DISTANCE,
                    LOOKUP_FILTER_GEO_POLYGON,

                ],
            },
        }
        # Define ordering fields
        ordering_fields = {
            'id': None,
            'street': None,
            'city': 'city.name.raw',
            'country': 'city.country.name.raw',
            'zip_code': None,
        }
        # Define ordering fields
        geo_spatial_ordering_fields = {
            'location': None,
        }
        # Specify default ordering
        ordering = (
            'id',
            'street.raw',
            'city.name.raw',
        )
        # Suggester fields
        suggester_fields = {
            'street_suggest': {
                'field': 'street.suggest',
                'suggesters': [
                    SUGGESTER_COMPLETION,
                ],
            },
            'city_suggest': {
                'field': 'city.name.suggest',
                'suggesters': [
                    SUGGESTER_COMPLETION,
                ],
            },
            'country_suggest': {
                'field': 'city.country.name.suggest',
                'suggesters': [
                    SUGGESTER_COMPLETION,
                ],
            }
        }

        # Facets
        faceted_search_fields = {
            'city': {
                'field': 'city.name.raw',
                'enabled': True,
            },
            'country': {
                'field': 'city.country.name.raw',
                'enabled': True,
            },
        }
