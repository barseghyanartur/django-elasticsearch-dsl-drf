====================
Basic usage examples
====================

Basic Django REST framework integration example

See the `example project
<https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/tree/master/examples/simple>`_
for sample models/views/serializers.

- `models
  <https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/blob/master/examples/simple/books/models.py>`_
- `documents
  <https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/blob/master/examples/simple/search_indexes/documents/book.py>`_
- `serializers
  <https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/blob/master/examples/simple/search_indexes/serializers/__init__.py>`_
- `views
  <https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/blob/master/examples/simple/search_indexes/viewsets/__init__.py>`_

Contents:

.. contents:: Table of Contents

Example app
===========

Sample models
-------------

*books/models/publisher.py*

.. code-block:: python

    class Publisher(models.Model):
        """Publisher."""

        name = models.CharField(max_length=30)
        address = models.CharField(max_length=50)
        city = models.CharField(max_length=60)
        state_province = models.CharField(max_length=30)
        country = models.CharField(max_length=50)
        website = models.URLField()
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

        class Meta:
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

Sample document
---------------

*search_indexes/documents/publisher.py*

.. code-block:: python

    from django_elasticsearch_dsl import Document, Index, fields
    from elasticsearch_dsl import analyzer

    from books.models import Publisher

    # Name of the Elasticsearch index
    PUBLISHER_INDEX = Index('publisher')
    # See Elasticsearch Indices API reference for available settings
    PUBLISHER_INDEX.settings(
        number_of_shards=1,
        number_of_replicas=1
    )

    @PUBLISHER_INDEX.doc_type
    class PublisherDocument(Document):
        """Publisher Elasticsearch document."""

        id = fields.IntegerField(attr='id')

        name = fields.StringField(
            fields={
                'raw': fields.StringField(analyzer='keyword'),
            }
        )
        info = fields.StringField(
            fields={
                'raw': fields.StringField(analyzer='keyword'),
            }
        )
        address = fields.StringField(
            fields={
                'raw': fields.StringField(analyzer='keyword'),
            }
        )
        city = fields.StringField(
            fields={
                'raw': fields.StringField(analyzer='keyword'),
            }
        )
        state_province = fields.StringField(
            fields={
                'raw': fields.StringField(analyzer='keyword'),
            }
        )
        country = fields.StringField(
            fields={
                'raw': fields.StringField(analyzer='keyword'),
            }
        )
        website = fields.StringField()

        # Location
        location = fields.GeoPointField(attr='location_field_indexing')

        class Meta:
            """Meta options."""

            model = Publisher  # The model associate with this Document


Sample serializer
-----------------

*search_indexes/serializers/book.py*

.. code-block:: python

    import json

    from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

    class PublisherDocumentSerializer(DocumentSerializer):
        """Serializer for Publisher document."""

        location = serializers.SerializerMethodField()

        class Meta:
            """Meta options."""

            # Note, that since we're using a dynamic serializer,
            # we only have to declare fields that we want to be shown. If
            # somehow, dynamic serializer doesn't work for you, either extend
            # or declare your serializer explicitly.
            fields = (
                'id',
                'name',
                'info',
                'address',
                'city',
                'state_province',
                'country',
                'website',
            )

        def get_location(self, obj):
        """Represent location value."""
        try:
            return obj.location.to_dict()
        except:
            return {}

Sample view
-----------

*search_indexes/views/publisher.py*

.. code-block:: python

    from django_elasticsearch_dsl_drf.constants import (
        LOOKUP_FILTER_GEO_DISTANCE,
    )
    from django_elasticsearch_dsl_drf.filter_backends import (
        FilteringFilterBackend,
        OrderingFilterBackend,
        SearchFilterBackend,
    )
    from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

    # Example app models
    from search_indexes.documents.publisher import PublisherDocument
    from search_indxes.serializers import PublisherDocumentSerializer

    class PublisherDocumentView(DocumentViewSet):
        """The PublisherDocument view."""

        document = PublisherDocument
        serializer_class = PublisherDocumentSerializer
        lookup_field = 'id'
        filter_backends = [
            FilteringFilterBackend,
            OrderingFilterBackend,
            DefaultOrderingFilterBackend,
            SearchFilterBackend,
        ]
        # Define search fields
        search_fields = (
            'name',
            'info',
            'address',
            'city',
            'state_province',
            'country',
        )
        # Define filtering fields
        filter_fields = {
            'id': None,
            'name': 'name.raw',
            'city': 'city.raw',
            'state_province': 'state_province.raw',
            'country': 'country.raw',
        }
        # Define ordering fields
        ordering_fields = {
            'id': None,
            'name': None,
            'city': None,
            'country': None,
        }
        # Specify default ordering
        ordering = ('id', 'name',)
        # Define geo-spatial filtering fields
        geo_spatial_filter_fields = {
            'location': {
                'lookups': [
                    LOOKUP_FILTER_GEO_DISTANCE,
                ],
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
Query param name reserved for search is ``search``. Make sure your models and
documents do not have it as a field or attribute.

Multiple search terms are joined with ``OR``.

Let's assume we have a number of Book items with fields ``title``,
``description`` and ``summary``.

**Search in all fields**

Search in all fields (``name``, ``address``, ``city``, ``state_province`` and
``country``) for word "reilly".

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?search=reilly

**Search a single term on specific field**

In order to search in specific field (``name``) for term "reilly", add
the field name separated with ``:`` to the search term.

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?search=name:reilly

**Search for multiple terms**

In order to search for multiple terms "reilly", "bloomsbury" add
multiple ``search`` query params.

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?search=reilly&search=bloomsbury

**Search for multiple terms in specific fields**

In order to search for multiple terms "reilly", "bloomsbury" in specific
fields add multiple ``search`` query params and field names separated with
``:`` to each of the search terms.

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?search=name:reilly&search=city:london

Filtering
^^^^^^^^^

Let's assume we have a number of Publisher documents with in cities (Yerevan,
Groningen, Amsterdam, London).

Multiple filter terms are joined with ``AND``.

**Filter documents by single field**

Filter documents by field (``city``) "yerevan".

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?city=yerevan

**Filter documents by multiple fields**

Filter documents by ``city`` "Yerevan" and "Groningen".

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?city__in=yerevan__groningen

**Filter document by a single field**

Filter documents by (field ``country``) "Armenia".

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?country=armenia

**Filter documents by multiple fields**

Filter documents by multiple fields (field ``city``) "Yerevan" and "Amsterdam"
with use of functional ``in`` query filter.

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?city__in=yerevan__amsterdam

You can achieve the same effect by specifying multiple filters (``city``)
"Yerevan" and "Amsterdam". Note, that in this case multiple filter terms are
joined with ``OR``.

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?city=yerevan&city=amsterdam

If you want the same as above, but joined with ``AND``, add ``__term`` to each
lookup.

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?city__term=education&city__term=economy

**Filter documents by a word part of a single field**

Filter documents by a part word part in single field (``city``) "ondon".

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?city__wildcard=*ondon


**Geo-distance filtering**

Filter documents by radius of 100000km from the given location.

.. code-block:: text

    http://127.0.0.1:8000/search/publishers/?location__geo_distance=100000km__12.04__-63.93

Ordering
^^^^^^^^

The ``-`` prefix means ordering should be descending.

**Order documents by field (ascending)**

Filter documents by field ``city`` (ascending).

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?search=country:armenia&ordering=city

**Order documents by field (descending)**

Filter documents by field ``country`` (descending).

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?ordering=-country

**Order documents by multiple fields**

If you want to order by multiple fields, use multiple ordering query params. In
the example below, documents would be ordered first by field ``country``
(descending), then by field ``city`` (ascending).

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?ordering=-country&ordering=city
