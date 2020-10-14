=======================
Advanced usage examples
=======================

Advanced Django REST framework integration examples.

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

*books/models/publisher.py*

.. code-block:: python

    import json

    from django.conf import settings
    from django.db import models
    from django.utils.translation import ugettext, ugettext_lazy as _

    from six import python_2_unicode_compatible

    BOOK_PUBLISHING_STATUS_PUBLISHED = 'published'
    BOOK_PUBLISHING_STATUS_NOT_PUBLISHED = 'not_published'
    BOOK_PUBLISHING_STATUS_IN_PROGRESS = 'in_progress'
    BOOK_PUBLISHING_STATUS_CANCELLED = 'cancelled'
    BOOK_PUBLISHING_STATUS_REJECTED = 'rejected'
    BOOK_PUBLISHING_STATUS_CHOICES = (
        (BOOK_PUBLISHING_STATUS_PUBLISHED, "Published"),
        (BOOK_PUBLISHING_STATUS_NOT_PUBLISHED, "Not published"),
        (BOOK_PUBLISHING_STATUS_IN_PROGRESS, "In progress"),
        (BOOK_PUBLISHING_STATUS_CANCELLED, "Cancelled"),
        (BOOK_PUBLISHING_STATUS_REJECTED, "Rejected"),
    )
    BOOK_PUBLISHING_STATUS_DEFAULT = BOOK_PUBLISHING_STATUS_PUBLISHED


    @python_2_unicode_compatible
    class Publisher(models.Model):
        """Publisher."""

        name = models.CharField(max_length=30)
        info = models.TextField(null=True, blank=True)
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

*books/models/author.py*

.. code-block:: python

    @python_2_unicode_compatible
    class Author(models.Model):
        """Author."""

        salutation = models.CharField(max_length=10)
        name = models.CharField(max_length=200)
        email = models.EmailField()
        headshot = models.ImageField(upload_to='authors', null=True, blank=True)

        class Meta(object):
            """Meta options."""

            ordering = ["id"]

        def __str__(self):
            return self.name

*books/models/tag.py*

.. code-block:: python

    class Tag(models.Model):
        """Simple tag model."""

        title = models.CharField(max_length=255, unique=True)

        class Meta(object):
            """Meta options."""

            verbose_name = _("Tag")
            verbose_name_plural = _("Tags")

        def __str__(self):
            return self.title

*books/models/book.py*

.. code-block:: python

    @python_2_unicode_compatible
    class Book(models.Model):
        """Book."""

        title = models.CharField(max_length=100)
        description = models.TextField(null=True, blank=True)
        summary = models.TextField(null=True, blank=True)
        authors = models.ManyToManyField('books.Author', related_name='books')
        publisher = models.ForeignKey(Publisher, related_name='books')
        publication_date = models.DateField()
        state = models.CharField(max_length=100,
                                 choices=BOOK_PUBLISHING_STATUS_CHOICES,
                                 default=BOOK_PUBLISHING_STATUS_DEFAULT)
        isbn = models.CharField(max_length=100, unique=True)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        pages = models.PositiveIntegerField(default=200)
        stock_count = models.PositiveIntegerField(default=30)
        tags = models.ManyToManyField('books.Tag',
                                      related_name='books',
                                      blank=True)

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
        'search_indexes.documents.book': 'book',
        'search_indexes.documents.publisher': 'publisher',
    }

*settings/testing.py*

.. code-block:: python

    # Name of the Elasticsearch index
    ELASTICSEARCH_INDEX_NAMES = {
        'search_indexes.documents.book': 'test_book',
        'search_indexes.documents.publisher': 'test_publisher',
    }

*settings/production.py*

.. code-block:: python

    # Name of the Elasticsearch index
    ELASTICSEARCH_INDEX_NAMES = {
        'search_indexes.documents.book': 'prod_book',
        'search_indexes.documents.publisher': 'prod_publisher',
    }

Document index
^^^^^^^^^^^^^^

*search_indexes/documents/book.py*

.. code-block:: python

    from django.conf import settings
    from django_elasticsearch_dsl import Document, Index, fields
    from elasticsearch_dsl import analyzer

    from books.models import Book

    # Name of the Elasticsearch index
    INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

    # See Elasticsearch Indices API reference for available settings
    INDEX.settings(
        number_of_shards=1,
        number_of_replicas=1
    )

    html_strip = analyzer(
        'html_strip',
        tokenizer="standard",
        filter=["standard", "lowercase", "stop", "snowball"],
        char_filter=["html_strip"]
    )


    @INDEX.doc_type
    class BookDocument(Document):
        """Book Elasticsearch document."""

        id = fields.IntegerField(attr='id')

        title = fields.StringField(
            analyzer=html_strip,
            fields={
                'raw': fields.StringField(analyzer='keyword'),
            }
        )

        description = fields.StringField(
            analyzer=html_strip,
            fields={
                'raw': fields.StringField(analyzer='keyword'),
            }
        )

        summary = fields.StringField(
            analyzer=html_strip,
            fields={
                'raw': fields.StringField(analyzer='keyword'),
            }
        )

        publisher = fields.StringField(
            attr='publisher_indexing',
            analyzer=html_strip,
            fields={
                'raw': fields.StringField(analyzer='keyword'),
            }
        )

        publication_date = fields.DateField()

        state = fields.StringField(
            analyzer=html_strip,
            fields={
                'raw': fields.StringField(analyzer='keyword'),
            }
        )

        isbn = fields.StringField(
            analyzer=html_strip,
            fields={
                'raw': fields.StringField(analyzer='keyword'),
            }
        )

        price = fields.FloatField()

        pages = fields.IntegerField()

        stock_count = fields.IntegerField()

        tags = fields.StringField(
            attr='tags_indexing',
            analyzer=html_strip,
            fields={
                'raw': fields.StringField(analyzer='keyword', multi=True),
                'suggest': fields.CompletionField(multi=True),
            },
            multi=True
        )

        class Meta(object):
            """Meta options."""

            model = Book  # The model associate with this Document

Sample serializer
-----------------

*search_indexes/serializers/tag.py*

.. code-block:: python

    import json

    from rest_framework import serializers

    class TagSerializer(serializers.Serializer):
        """Helper serializer for the Tag field of the Book document."""

        title = serializers.CharField()

        class Meta(object):
            """Meta options."""

            fields = ('title',)
            read_only_fields = ('title',)

*search_indexes/serializers/book.py*

.. code-block:: python

    class BookDocumentSerializer(serializers.Serializer):
        """Serializer for the Book document."""

        id = serializers.SerializerMethodField()

        title = serializers.CharField(read_only=True)
        description = serializers.CharField(read_only=True)
        summary = serializers.CharField(read_only=True)

        publisher = serializers.CharField(read_only=True)
        publication_date = serializers.DateField(read_only=True)
        state = serializers.CharField(read_only=True)
        isbn = serializers.CharField(read_only=True)
        price = serializers.FloatField(read_only=True)
        pages = serializers.IntegerField(read_only=True)
        stock_count = serializers.IntegerField(read_only=True)
        tags = serializers.SerializerMethodField()

        class Meta(object):
            """Meta options."""

            fields = (
                'id',
                'title',
                'description',
                'summary',
                'publisher',
                'publication_date',
                'state',
                'isbn',
                'price',
                'pages',
                'stock_count',
                'tags',
            )
            read_only_fields = fields

        def get_tags(self, obj):
            """Get tags."""
            if obj.tags:
                return list(obj.tags)
            else:
                return []

Sample view
-----------

*search_indexes/viewsets/book.py*

.. code-block:: python

    from django_elasticsearch_dsl_drf.constants import (
        LOOKUP_FILTER_TERMS,
        LOOKUP_FILTER_RANGE,
        LOOKUP_FILTER_PREFIX,
        LOOKUP_FILTER_WILDCARD,
        LOOKUP_QUERY_IN,
        LOOKUP_QUERY_EXCLUDE,
    )
    from django_elasticsearch_dsl_drf.filter_backends import (
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    )
    from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

    # Example app models
    from search_indexes.documents.book import BookDocument
    from search_indxes.serializers import BookDocumentSerializer


    class BookDocumentView(DocumentViewSet):
        """The BookDocument view."""

        document = BookDocument
        serializer_class = BookDocumentSerializer
        lookup_field = 'id'
        filter_backends = [
            FilteringFilterBackend,
            OrderingFilterBackend,
            DefaultOrderingFilterBackend,
            SearchFilterBackend,
        ]
        # Define search fields
        search_fields = (
            'title',
            'summary',
            'description',
        )
        # Define filtering fields
        filter_fields = {
            'id': {
                'field': '_id',
                'lookups': [
                    LOOKUP_FILTER_RANGE,
                    LOOKUP_QUERY_IN,
                ],
            },
            'publisher': 'publisher.raw',
            'publication_date': 'publication_date',
            'isbn': 'isbn.raw',
            'tags': {
                'field': 'tags',
                'lookups': [
                    LOOKUP_FILTER_TERMS,
                    LOOKUP_FILTER_PREFIX,
                    LOOKUP_FILTER_WILDCARD,
                    LOOKUP_QUERY_IN,
                    LOOKUP_QUERY_EXCLUDE,
                ],
            },
            'tags.raw': {
                'field': 'tags.raw',
                'lookups': [
                    LOOKUP_FILTER_TERMS,
                    LOOKUP_FILTER_PREFIX,
                    LOOKUP_FILTER_WILDCARD,
                    LOOKUP_QUERY_IN,
                    LOOKUP_QUERY_EXCLUDE,
                ],
            },
        }
        # Define ordering fields
        ordering_fields = {
            'id': 'id',
            'title': 'title.raw',
            'price': 'price.raw',
            'state': 'state.raw',
            'publication_date': 'publication_date',
        }
        # Specify default ordering
        ordering = ('id', 'title',)

Usage example
-------------

Considering samples above, you should be able to perform the search, sorting
and filtering actions described below.

Search
~~~~~~

Query param name reserved for search is ``search``. Make sure your models and
documents do not have it as a field or attribute.

Multiple search terms are joined with ``OR``.

Let's assume we have a number of Book items with fields ``title``,
``description`` and ``summary``.

**Search in all fields**

Search in all fields (``title``, ``description`` and ``summary``) for word
"education".

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=education

**Search a single term on specific field**

In order to search in specific field (``title``) for term "education", add
the field name separated with ``:`` to the search term.

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=title:education

**Search for multiple terms**

In order to search for multiple terms "education", "technology" add
multiple ``search`` query params.

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=education&search=technology

**Search for multiple terms on specific fields**

In order to search for multiple terms "education", "technology" in specific
fields add multiple ``search`` query params and field names separated with
``:`` to each of the search terms.

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=title:education&search=summary:technology

**Search with boosting**

It's possible to boost search fields. In order to do that change the
`search_fields` definition of the `DocumentViewSet` as follows:

.. code-block:: python

    class BookDocumentView(DocumentViewSet):
        """The BookDocument view."""

        # ...

        # Define search fields
        search_fields = {
            'title': {'boost': 4},
            'summary': {'boost': 2},
            'description': None,
        }

        # Order by `_score` first.
        ordering = ('_score', 'id', 'title', 'price',)

        # ...

Note, that we are ordering results by `_score` first.

Filtering
~~~~~~~~~

Let's assume we have a number of Book documents with the tags (education,
politics, economy, biology, climate, environment, internet, technology).

Multiple filter terms are joined with ``AND``.

**Filter documents by field**

Filter documents by field (``state``) "published".

.. code-block:: text

    http://127.0.0.1:8080/search/books/?state=published

**Filter documents by multiple fields**

Filter documents by field (``states``) "published" and "in_progress".

.. code-block:: text

    http://127.0.0.1:8080/search/books/?state__in=published__in_progress

**Filter document by a single field**

Filter documents by (field ``tag``) "education".

.. code-block:: text

    http://127.0.0.1:8080/search/books/?tag=education

**Filter documents by multiple fields**

Filter documents by multiple fields (field ``tags``) "education" and "economy"
with use of functional ``in`` query filter.

.. code-block:: text

    http://127.0.0.1:8080/search/books/?tags__in=education__economy

You can achieve the same effect by specifying multiple fields (``tags``)
"education" and "economy". Note, that in this case multiple filter terms are
joined with ``OR``.

.. code-block:: text

    http://127.0.0.1:8080/search/books/?tags=education&tags=economy

If you want the same as above, but joined with ``AND``, add ``__term`` to each
lookup.

.. code-block:: text

    http://127.0.0.1:8080/search/books/?tags__term=education&tags__term=economy

**Filter documents by a word part of a single field**

Filter documents by a part word part in single field (``tags``). Word part
should match both "technology" and "biology".

.. code-block:: text

    http://127.0.0.1:8080/search/books/?tags__wildcard=*logy

Ordering
~~~~~~~~

The ``-`` prefix means ordering should be descending.

**Order documents by field (ascending)**

Order documents by field ``price`` (ascending).

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=title:lorem&ordering=price

**Order documents by field (descending)**

Order documents by field ``price`` (descending).

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=title:lorem&ordering=-price

**Order documents by multiple fields**

If you want to order by multiple fields, use multiple ordering query params. In
the example below, documents would be ordered first by field
``publication_date`` (descending), then by field ``price`` (ascending).

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=title:lorem&ordering=-publication_date&ordering=price

Ids filter
----------
Filters documents that only have the provided ids.

.. code-block:: text

    http://127.0.0.1:8000/api/articles/?ids=68__64__58

Or, alternatively:

.. code-block:: text

    http://127.0.0.1:8000/api/articles/?ids=68&ids=64&ids=58

Faceted search
--------------

In order to add faceted search support, we would have to extend our
view set in the following way:

*search_indexes/viewsets/book.py*

.. code-block:: python

    # ...

    from django_elasticsearch_dsl_drf.filter_backends import (
        # ...
        FacetedSearchFilterBackend,
    )

    # ...

    from elasticsearch_dsl import (
        DateHistogramFacet,
        RangeFacet,
        TermsFacet,
    )

    # ...

    class BookDocumentView(DocumentViewSet):
        """The BookDocument view."""

        # ...

        filter_backends = [
            # ...
            FacetedSearchFilterBackend,
        ]

        # ...

        faceted_search_fields = {
            'state': 'state.raw',  # By default, TermsFacet is used
            'publisher': {
                'field': 'publisher.raw',
                'facet': TermsFacet,  # But we can define it explicitly
                'enabled': True,
            },
            'publication_date': {
                'field': 'publication_date',
                'facet': DateHistogramFacet,
                'options': {
                    'interval': 'year',
                }
            },
            'pages_count': {
                'field': 'pages',
                'facet': RangeFacet,
                'options': {
                    'ranges': [
                        ("<10", (None, 10)),
                        ("11-20", (11, 20)),
                        ("20-50", (20, 50)),
                        (">50", (50, None)),
                    ]
                }
            },
        }

        # ...

Note, that none of the facets is enabled by default, unless you
explicitly specify it to be enabled. That means, that you will have to
add a query string `facet={facet_field_name}` for each of the facets
you want to see in results.

In the example below, we show results with faceted ``state`` and
``pages_count`` facets.

.. code-block:: text

    http://127.0.0.1:8000/search/books/?facet=state&facet=pages_count

Post-filter
-----------
The `post_filter` is very similar to the common filter. The only difference
is that it doesn't affect facets. So, whatever post-filters applied, the
numbers in facets will remain intact.

Sample view
~~~~~~~~~~~
.. note::

    Note the ``PostFilterFilteringFilterBackend`` and ``post_filter_fields``
    usage.

*search_indexes/viewsets/book.py*

.. code-block:: python

    # ...

    from django_elasticsearch_dsl_drf.filter_backends import (
        # ...
        PostFilterFilteringFilterBackend,
    )

    # ...

    class BookDocumentView(DocumentViewSet):
        """The BookDocument view."""

        document = BookDocument
        serializer_class = BookDocumentSerializer
        lookup_field = 'id'
        filter_backends = [
            FilteringFilterBackend,
            OrderingFilterBackend,
            DefaultOrderingFilterBackend,
            SearchFilterBackend,
            PostFilterFilteringFilterBackend,
        ]
        # Define search fields
        search_fields = (
            'title',
            'summary',
            'description',
        )
        # Define filtering fields
        filter_fields = {
            'id': {
                'field': '_id',
                'lookups': [
                    LOOKUP_FILTER_RANGE,
                    LOOKUP_QUERY_IN,
                ],
            },
            'publisher': 'publisher.raw',
            'publication_date': 'publication_date',
            'isbn': 'isbn.raw',
            'tags': {
                'field': 'tags',
                'lookups': [
                    LOOKUP_FILTER_TERMS,
                    LOOKUP_FILTER_PREFIX,
                    LOOKUP_FILTER_WILDCARD,
                    LOOKUP_QUERY_IN,
                    LOOKUP_QUERY_EXCLUDE,
                ],
            },
            'tags.raw': {
                'field': 'tags.raw',
                'lookups': [
                    LOOKUP_FILTER_TERMS,
                    LOOKUP_FILTER_PREFIX,
                    LOOKUP_FILTER_WILDCARD,
                    LOOKUP_QUERY_IN,
                    LOOKUP_QUERY_EXCLUDE,
                ],
            },
        }
        # Define post-filter filtering fields
        post_filter_fields = {
            'publisher_pf': 'publisher.raw',
            'isbn_pf': 'isbn.raw',
            'state_pf': 'state.raw',
            'tags_pf': {
                'field': 'tags',
                'lookups': [
                    LOOKUP_FILTER_TERMS,
                    LOOKUP_FILTER_PREFIX,
                    LOOKUP_FILTER_WILDCARD,
                    LOOKUP_QUERY_IN,
                    LOOKUP_QUERY_EXCLUDE,
                ],
            },
        }
        # Define ordering fields
        ordering_fields = {
            'id': 'id',
            'title': 'title.raw',
            'price': 'price.raw',
            'state': 'state.raw',
            'publication_date': 'publication_date',
        }
        # Specify default ordering
        ordering = ('id', 'title',)

Sample queries
~~~~~~~~~~~~~~

**Filter documents by field**

Filter documents by field (``state``) "published".

.. code-block:: text

    http://127.0.0.1:8080/search/books/?state_pf=published

**Filter documents by multiple fields**

Filter documents by field (``states``) "published" and "in_progress".

.. code-block:: text

    http://127.0.0.1:8080/search/books/?state_pf__in=published__in_progress

Geo-spatial features
--------------------

For testing the boundaries the following online services might be helpful:

- `geojson.io <http://geojson.io>`_
- `Bounding Box Tool <http://boundingbox.klokantech.com>`_

Filtering
~~~~~~~~~

**Geo-distance filtering**

Filter documents by radius of 100000km from the given location.

.. code-block:: text

    http://localhost:8000/search/publishers/?location__geo_distance=100000km__12.04__-63.93

**Geo-polygon filtering**

Filter documents that are located in the given polygon.

.. code-block:: text

    http://localhost:8000/search/publishers/?location__geo_polygon=40,-70__30,-80__20,-90

**Geo-bounding-box filtering**

Filter documents that are located in the given bounding box.

.. code-block:: text

    http://localhost:8000/search/publishers/?location__geo_bounding_box=44.87,40.07__43.87,41.11

Ordering
~~~~~~~~

**Geo-distance ordering**

.. code-block:: text

    http://localhost:8000/search/publishers/?ordering=location__48.85__2.30__km__plane

Geo-shape
~~~~~~~~

**Setup**

In order to be able to do all geo-shape queries, you need a GeoShapeField with 'recursive' strategy.
Details about spatial strategies here : https://www.elastic.co/guide/en/elasticsearch/reference/master/geo-shape.html#spatial-strategy

.. code-block:: python

        # ...

        @INDEX.doc_type
        class PublisherDocument(Document):

        # ...

            location_circle = fields.GeoShapeField(strategy='recursive',
                                                   attr='location_circle_indexing')

        # ...

        class Publisher(models.Model):

        # ...

            @property
            def location_circle_indexing(self):
                """
                Indexing circle geo_shape with 10km radius.
                Used in Elasticsearch indexing/tests of `geo_shape` native filter.
                """
                return {
                    'type': 'circle',
                    'coordinates': [self.latitude, self.longitude],
                    'radius': '10km',
                }


You need to use GeoSpatialFilteringFilterBackend and set the LOOKUP_FILTER_GEO_SHAPE to the geo_spatial_filter_field. (This takes place in ViewSet)

.. code-block:: python

        # ...
        class PublisherDocumentViewSet(DocumentViewSet):
        # ...
            filter_backends = [
                # ...
                GeoSpatialFilteringFilterBackend,
                # ...
            ]
        # ...
            geo_spatial_filter_fields = {
                # ...
                'location_circle': {
                    'lookups': [
                        LOOKUP_FILTER_GEO_SHAPE,
                    ]
                },
                # ...
            }
        # ...


**Supported shapes & queries**

With this setup, we can do several types of Geo-shape queries.

Supported and tested shapes types are : point, circle, envelope

Pottentially supported but untested shapes are : multipoint and linestring

Supported and tested queries are : INTERSECTS, DISJOINT, WITHIN, CONTAINS

**Shapes intersects**

Interesting queries are shape intersects : this gives you all documents whose shape intersects with the shape given in query. (Should be 2 with the actual test dataset)

.. code-block:: text

    http://localhost:8000/search/publishers/?location_circle__geo_shape=49.119696,6.176355__radius,15km__relation,intersects__type,circle

This request give you all publishers having a location_circle intersecting with the one in the query.


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

Completion suggesters
~~~~~~~~~~~~~~~~~~~~~

Document definition
^^^^^^^^^^^^^^^^^^^

To make use of suggestions, you should properly index relevant fields of your
documents using ``fields.CompletionField``.

*search_indexes/documents/publisher.py*

.. code-block:: python

    from django.conf import settings

    from django_elasticsearch_dsl import Document, Index, fields

    from books.models import Publisher

    # Name of the Elasticsearch index
    INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

    # See Elasticsearch Indices API reference for available settings
    INDEX.settings(
        number_of_shards=1,
        number_of_replicas=1
    )


    @INDEX.doc_type
    class PublisherDocument(Document):
        """Publisher Elasticsearch document."""

        id = fields.IntegerField(attr='id')

        name = fields.StringField(
            fields={
                'raw': fields.StringField(analyzer='keyword'),
                'suggest': fields.CompletionField(),
            }
        )

        info = fields.StringField()

        address = fields.StringField(
            fields={
                'raw': fields.StringField(analyzer='keyword')
            }
        )

        city = fields.StringField(
            fields={
                'raw': fields.StringField(analyzer='keyword'),
                'suggest': fields.CompletionField(),
            }
        )

        state_province = fields.StringField(
            fields={
                'raw': fields.StringField(analyzer='keyword'),
                'suggest': fields.CompletionField(),
            }
        )

        country = fields.StringField(
            fields={
                'raw': fields.StringField(analyzer='keyword'),
                'suggest': fields.CompletionField(),
            }
        )

        website = fields.StringField()

        # Location
        location = fields.GeoPointField(attr='location_field_indexing')

        class Meta(object):
            """Meta options."""

            model = Publisher  # The model associate with this Document

After that the ``name.suggest``, ``city.suggest``, ``state_province.suggest``
and ``country.suggest`` fields would be available for suggestions feature.

Serializer definition
^^^^^^^^^^^^^^^^^^^^^

This is how publisher serializer would look like.

*search_indexes/serializers/publisher.py*

.. code-block:: python

    import json

    from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

    class PublisherDocumentSerializer(DocumentSerializer):
        """Serializer for Publisher document."""

        class Meta(object):
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

ViewSet definition
^^^^^^^^^^^^^^^^^^

In order to add suggestions support, we would have to extend our view set in
the following way:

.. note:: You should inherit from `DocumentViewSet` instead of `BaseDocumentViewSet`.

*search_indexes/viewsets/publisher.py*

.. code-block:: python

    # ...

    from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
    from django_elasticsearch_dsl_drf.filter_backends import (
        # ...
        SuggesterFilterBackend,
    )

    # ...

    class PublisherDocumentViewSet(DocumentViewSet):
        """The PublisherDocument view."""

        document = PublisherDocument

        # ...

        filter_backends = [
            # ...
            SuggesterFilterBackend,
        ]

        # ...

        # Suggester fields
        suggester_fields = {
            'name_suggest': {
                'field': 'name.suggest',
                'suggesters': [
                    SUGGESTER_COMPLETION,
                ],
                'options': {
                    'size': 20,  # Override default number of suggestions
                    'skip_duplicates':True, # Whether duplicate suggestions should be filtered out.
                },
            },
            'city_suggest': {
                'field': 'city.suggest',
                'suggesters': [
                    SUGGESTER_COMPLETION,
                ],
            },
            'state_province_suggest': {
                'field': 'state_province.suggest',
                'suggesters': [
                    SUGGESTER_COMPLETION,
                ],
            },
            'country_suggest': {
                'field': 'country.suggest',
                'suggesters': [
                    SUGGESTER_COMPLETION,
                ],
            },
        }

        # Geo-spatial filtering fields
        geo_spatial_filter_fields = {
            'location': {
                'lookups': [
                    LOOKUP_FILTER_GEO_DISTANCE,
                ],
            },
        }

In the example below, we show suggestion results (auto-completion) for
``country`` field.

Sample requests/responses
^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have extended your view set with ``SuggesterFilterBackend``
functionality, you can make use of the ``suggest`` custom action of your
view set.

**Request**

.. code-block:: text

    GET http://127.0.0.1:8000/search/publishers/suggest/?country_suggest__completion=Ar

**Response**

.. code-block:: javascript

    {
        "_shards": {
            "failed": 0,
            "successful": 1,
            "total": 1
        },
        "country_suggest__completion": [
            {
                "options": [
                    {
                        "score": 1.0,
                        "text": "Armenia"
                    },
                    {
                        "score": 1.0,
                        "text": "Argentina"
                    }
                ],
                "offset": 0,
                "length": 2,
                "text": "Ar"
            }
        ]
    }

You can also have multiple suggesters per request.

**Request**

.. code-block:: text

    GET http://127.0.0.1:8000/search/publishers/suggest/?name_suggest__completion=B&country_suggest__completion=Ar

**Response**

.. code-block:: javascript

    {
        "_shards": {
            "successful": 1,
            "total": 1,
            "failed": 0
        },
        "country_suggest__completion": [
            {
                "text": "Ar",
                "options": [
                    {
                        "score": 1.0,
                        "text": "Armenia"
                    },
                    {
                        "score": 1.0,
                        "text": "Argentina"
                    }
                ],
                "offset": 0,
                "length": 2
            }
        ],
        "name_suggest__completion": [
            {
                "text": "B",
                "options": [
                    {
                        "score": 1.0,
                        "text": "Book Works"
                    },
                    {
                        "score": 1.0,
                        "text": "Brumleve LLC"
                    },
                    {
                        "score": 1.0,
                        "text": "Booktrope"
                    },
                    {
                        "score": 1.0,
                        "text": "Borman, Post and Wendt"
                    },
                    {
                        "score": 1.0,
                        "text": "Book League of America"
                    }
                ],
                "offset": 0,
                "length": 1
            }
        ]
    }

Suggestions on Array/List field
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Suggestions on Array/List fields (typical use case - tags, where Tag model
would be a many-to-many relation to a Book model) work almost the
same.

Before checking the `Sample requests/responses`, do have in mind the following:

- ``Book`` (see the `Sample models`_)
- ``BookSerializer`` (see the `Sample serializer`_)
- ``BookDocumentView`` (see the `Sample view`_)

Sample requests/responses
+++++++++++++++++++++++++

Once you have extended your view set with ``SuggesterFilterBackend``
functionality, you can make use of the ``suggest`` custom action of your
view set.

**Request**

.. code-block:: text

    GET http://127.0.0.1:8000/search/books/suggest/?tag_suggest__completion=bio

**Response**

.. code-block:: javascript

    {
        "_shards": {
            "failed": 0,
            "successful": 1,
            "total": 1
        },
        "tag_suggest__completion": [
            {
                "options": [
                    {
                        "score": 1.0,
                        "text": "Biography"
                    },
                    {
                        "score": 1.0,
                        "text": "Biology"
                    }
                ],
                "offset": 0,
                "length": 2,
                "text": "bio"
            }
        ]
    }

Context suggesters
^^^^^^^^^^^^^^^^^^
Note, that context suggesters only work for `completion` (thus, not for `term`
or `phrase`).

`category` context
++++++++++++++++++
The completion suggester considers all documents in the index, but it is often
desirable to serve suggestions filtered and/or boosted by some criteria. For
example, you want to suggest song titles filtered by certain artists or you
want to boost song titles based on their genre.

In that case, the document definition should be altered as follows:

**Document definition**

.. code-block:: python

    class BookDocument(Document):

        # ...

        title = StringField(
            analyzer=html_strip,
            fields={
                'raw': KeywordField(),
                'suggest': fields.CompletionField(),
                'suggest_context': fields.CompletionField(
                    contexts=[
                        {
                            "name": "tag",
                            "type": "category",
                            # The `path` value shall be pointing to an
                            # existing field of current document, which shall
                            # be used for filtering.
                            "path": "tags.raw",
                        },
                    ]
                ),
            }
        )

        # Tags
        tags = StringField(
            attr='tags_indexing',
            analyzer=html_strip,
            fields={
                'raw': KeywordField(multi=True),
                'suggest': fields.CompletionField(multi=True),
            },
            multi=True
        )

        # ...

ViewSet should altered as follows:

**ViewSet definition**

.. code-block:: python

    class BookFrontendDocumentViewSet(DocumentViewSet):

        # ...

        # Suggester fields
        suggester_fields = {
            'title_suggest_context': {
                'field': 'title.suggest_context',
                'default_suggester': SUGGESTER_COMPLETION,
                # We want to be able to filter the completion filter
                # results on the following params: tag, state and publisher.
                # We also want to provide the size value.
                # See the "https://www.elastic.co/guide/en/elasticsearch/
                # reference/6.1/suggester-context.html" for the reference.
                'completion_options': {
                    'category_filters': {
                        # The `tag` has been defined as `name` value in the
                        # `suggest_context` of the `BookDocument`.
                        'title_suggest_tag': 'tag',
                    },
                },
                'options': {
                    'size': 10,  # By default, number of results is 5.
                    'skip_duplicates':True, # Whether duplicate suggestions should be filtered out.
                },
            },
        }

        # ...

And finally we can narrow our suggestions as follows:

**Sample request**

In the example below we have filtered suggestions by tags "Art" and "Comics"
having boosted "Comics" by 2.0.

.. code-block:: text

    GET http://localhost:8000/search/books-frontend/suggest/?title_suggest_context=M&title_suggest_tag=Art&title_suggest_tag=Comics__2.0

`geo` context
+++++++++++++
Geo context allows to get suggestions within a certain distance from a
specified geo location.

In that case, the document definition should be altered as follows:

**Document definition**

.. code-block:: python

    class AddressDocument(Document):

        # ...

        street = StringField(
            analyzer=html_strip,
            fields={
                'raw': KeywordField(),
                'suggest': fields.CompletionField(),
                'suggest_context': fields.CompletionField(
                    contexts=[
                        {
                            "name": "loc",
                            "type": "geo",
                            "path": "location",
                            # You could also optionally add precision value.
                            # However, this is not required and can be
                            # specified in the query during runtime.
                            # "precision": "100km",
                        },
                    ],
                ),
            }
        )

        location = fields.GeoPointField(
            attr='location_field_indexing',
        )

        # ...

ViewSet should altered as follows:

**ViewSet definition**

.. code-block:: python

    class BookFrontendDocumentViewSet(DocumentViewSet):

        # ...

        # Suggester fields
        suggester_fields = {
            'street_suggest_context': {
                'field': 'street.suggest_context',
                'default_suggester': SUGGESTER_COMPLETION,
                # We want to be able to filter the completion filter
                # results on the following params: tag, state and publisher.
                # We also want to provide the size value.
                # See the "https://www.elastic.co/guide/en/elasticsearch/
                # reference/6.1/suggester-context.html" for the reference.
                'completion_options': {
                    'geo_filters': {
                        'title_suggest_loc': 'loc',
                    },
                },
                'options': {
                    'size': 10,  # By default, number of results is 5.
                    'skip_duplicates':True, # Whether duplicate suggestions should be filtered out.
                },
            },
        }

        # ...

And finally we can narrow our suggestions as follows:

**Sample request**

In the example below we have filtered suggestions within 8000km distance
from geo-point (-30, -100).

.. code-block:: text

    GET http://localhost:8000/search/addresses-frontend/suggest/?street_suggest_context=L&title_suggest_loc=-30__-100__8000km

Same query with boosting (boost value 2.0):

.. code-block:: text

    GET http://localhost:8000/search/addresses-frontend/suggest/?street_suggest_context=L&title_suggest_loc=-30__-100__8000km__2.0

Term and Phrase suggestions
~~~~~~~~~~~~~~~~~~~~~~~~~~~
While for the ``completion`` suggesters to work the ``CompletionField`` shall
be used, the ``term`` and ``phrase`` suggesters work on common text fields.

Document definition
^^^^^^^^^^^^^^^^^^^

*search_indexes/documents/book.py*

.. code-block:: python

    from django.conf import settings

    from django_elasticsearch_dsl import Document, Index, fields

    from books.models import Book

    # Name of the Elasticsearch index
    INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

    # See Elasticsearch Indices API reference for available settings
    INDEX.settings(
        number_of_shards=1,
        number_of_replicas=1
    )

    @INDEX.doc_type
    class BookDocument(Document):
        """Book Elasticsearch document."""
        # ID
        id = fields.IntegerField(attr='id')

        title = StringField(
            analyzer=html_strip,
            fields={
                'raw': KeywordField(),
                'suggest': fields.CompletionField(),
            }
        )

        description = StringField(
            analyzer=html_strip,
            fields={
                'raw': KeywordField(),
            }
        )

        summary = StringField(
            analyzer=html_strip,
            fields={
                'raw': KeywordField()
            }
        )

        # Publisher
        publisher = StringField(
            attr='publisher_indexing',
            analyzer=html_strip,
            fields={
                'raw': KeywordField(),
                'suggest': fields.CompletionField(),
            }
        )

        # Publication date
        publication_date = fields.DateField()

        # State
        state = StringField(
            analyzer=html_strip,
            fields={
                'raw': KeywordField(),
            }
        )

        # ISBN
        isbn = StringField(
            analyzer=html_strip,
            fields={
                'raw': KeywordField(),
            }
        )

        # Price
        price = fields.FloatField()

        # Pages
        pages = fields.IntegerField()

        # Stock count
        stock_count = fields.IntegerField()

        # Tags
        tags = StringField(
            attr='tags_indexing',
            analyzer=html_strip,
            fields={
                'raw': KeywordField(multi=True),
                'suggest': fields.CompletionField(multi=True),
            },
            multi=True
        )

        null_field = fields.StringField(attr='null_field_indexing')

        class Meta(object):
            """Meta options."""

            model = Book  # The model associate with this Document

ViewSet definition
^^^^^^^^^^^^^^^^^^

.. note:: The suggester filter backends shall come as last ones.

Suggesters for the view are configured in ``suggester_fields`` property.

In the example below, the ``title_suggest`` is the name of the GET query param
which points to the ``title.suggest`` field of the ``BookDocument`` document.
For the ``title_suggest`` the allowed suggesters are ``SUGGESTER_COMPLETION``,
``SUGGESTER_TERM`` and ``SUGGESTER_PHRASE``.

URL shall be constructed in the following way:

.. code-block:: text

    /search/books/suggest/?{QUERY_PARAM}__{SUGGESTER_NAME}={VALUE}

Example for ``completion`` suggester:

.. code-block:: text

    GET http://127.0.0.1:8000/search/books/suggest/?title_suggest__completion=temp

However, since we have ``default_suggester`` defined we can skip the
``__{SUGGESTER_NAME}`` part (if we want ``completion`` suggester
functionality). Thus, it might be written as short as:

.. code-block:: text

    GET http://127.0.0.1:8000/search/books/suggest/?title_suggest=temp

Example for ``term`` suggester:

.. code-block:: text

    GET http://127.0.0.1:8000/search/books/suggest/?title_suggest__term=tmeporus

Example for ``phrase`` suggester:

.. code-block:: text

    GET http://127.0.0.1:8000/search/books/suggest/?title_suggest__phrase=tmeporus

*search_indexes/viewsets/book.py*

.. code-block:: python

    from django_elasticsearch_dsl_drf.constants import (
        LOOKUP_FILTER_PREFIX,
        LOOKUP_FILTER_RANGE,
        LOOKUP_FILTER_TERMS,
        LOOKUP_FILTER_WILDCARD,
        LOOKUP_QUERY_EXCLUDE,
        LOOKUP_QUERY_GT,
        LOOKUP_QUERY_GTE,
        LOOKUP_QUERY_IN,
        LOOKUP_QUERY_IN,
        LOOKUP_QUERY_ISNULL,
        LOOKUP_QUERY_LT,
        LOOKUP_QUERY_LTE,
        SUGGESTER_COMPLETION,
        SUGGESTER_PHRASE,
        SUGGESTER_TERM,
    )
    from django_elasticsearch_dsl_drf.filter_backends import (
        # ...
        SuggesterFilterBackend,
    )

    class BookDocumentViewSet(DocumentViewSet):
        """The BookDocument view."""

        document = BookDocument
        # serializer_class = BookDocumentSerializer
        serializer_class = BookDocumentSimpleSerializer
        lookup_field = 'id'
        filter_backends = [
            FilteringFilterBackend,
            OrderingFilterBackend,
            DefaultOrderingFilterBackend,
            SearchFilterBackend,
            SuggesterFilterBackend,  # This should be the last backend
        ]
        # Define search fields
        search_fields = (
            'title',
            'description',
            'summary',
        )
        # Define filter fields
        filter_fields = {
            'id': {
                'field': 'id',
                'lookups': [
                    LOOKUP_FILTER_RANGE,
                    LOOKUP_QUERY_IN,
                    LOOKUP_QUERY_GT,
                    LOOKUP_QUERY_GTE,
                    LOOKUP_QUERY_LT,
                    LOOKUP_QUERY_LTE,
                    LOOKUP_FILTER_TERMS,
                ],
            },
            'title': 'title.raw',
            'publisher': 'publisher.raw',
            'publication_date': 'publication_date',
            'state': 'state.raw',
            'isbn': 'isbn.raw',
            'price': {
                'field': 'price.raw',
                'lookups': [
                    LOOKUP_FILTER_RANGE,
                ],
            },
            'pages': {
                'field': 'pages',
                'lookups': [
                    LOOKUP_FILTER_RANGE,
                    LOOKUP_QUERY_GT,
                    LOOKUP_QUERY_GTE,
                    LOOKUP_QUERY_LT,
                    LOOKUP_QUERY_LTE,
                ],
            },
            'stock_count': {
                # 'field': 'stock_count',
                'lookups': [
                    LOOKUP_FILTER_RANGE,
                    LOOKUP_QUERY_GT,
                    LOOKUP_QUERY_GTE,
                    LOOKUP_QUERY_LT,
                    LOOKUP_QUERY_LTE,
                ],
            },
            'tags': {
                'field': 'tags',
                'lookups': [
                    LOOKUP_FILTER_TERMS,
                    LOOKUP_FILTER_PREFIX,
                    LOOKUP_FILTER_WILDCARD,
                    LOOKUP_QUERY_IN,
                    LOOKUP_QUERY_EXCLUDE,
                    LOOKUP_QUERY_ISNULL,
                ],
            },
            'tags.raw': {
                'field': 'tags.raw',
                'lookups': [
                    LOOKUP_FILTER_TERMS,
                    LOOKUP_FILTER_PREFIX,
                    LOOKUP_FILTER_WILDCARD,
                    LOOKUP_QUERY_IN,
                    LOOKUP_QUERY_EXCLUDE,
                ],
            },
            # This has been added to test `exists` filter.
            'non_existent_field': 'non_existent_field',
            # This has been added to test `isnull` filter.
            'null_field': 'null_field',
        }
        # Define ordering fields
        ordering_fields = {
            'id': 'id',
            'title': 'title.raw',
            'price': 'price.raw',
            'state': 'state.raw',
            'publication_date': 'publication_date',
        }
        # Specify default ordering
        ordering = ('id', 'title', 'price',)

        # Suggester fields
        suggester_fields = {
            'title_suggest': {
                'field': 'title.suggest',
                'suggesters': [
                    SUGGESTER_COMPLETION,
                    SUGGESTER_TERM,
                    SUGGESTER_PHRASE,
                ]
                'default_suggester': SUGGESTER_COMPLETION,
                'options': {
                    'size': 10,  # Number of suggestions to retrieve.
                    'skip_duplicates':True, # Whether duplicate suggestions should be filtered out.
                },
            },
            'publisher_suggest': 'publisher.suggest',
            'tag_suggest': 'tags.suggest',
            'summary_suggest': 'summary',
        }

Note, that by default the number of suggestions is limited to 5. If you need
more suggestions, add 'options` dictionary with `size` provided, as show above.

Sample requests/responses
^^^^^^^^^^^^^^^^^^^^^^^^^
Once you have extended your view set with ``SuggesterFilterBackend``
functionality, you can make use of the ``suggest`` custom action of your
view set.

Let's considering, that one of our books has the following text in the summary:

.. code-block:: text

    Twas brillig, and the slithy toves
    Did gyre and gimble in the wabe.
    All mimsy were the borogoves
    And the mome raths outgrabe.

    "Beware the Jabberwock, my son!
    The jaws that bite, the claws that catch!
    Beware the Jubjub bird, and shun
    The frumious Bandersnatch!"

    He took his vorpal sword in his hand,
    Long time the manxome foe he sought --
    So rested he by the Tumtum tree,
    And stood awhile in thought.

Completion
++++++++++


**Request**

.. code-block:: text

    GET http://127.0.0.1:8000/search/books/suggest/?title_suggest__completion=temp

**Response**

.. code-block:: javascript

    {
        "_shards": {
            "successful": 1,
            "total": 1,
            "failed": 0
        },
        "title_suggest": [
            {
                "length": 4,
                "text": "temp",
                "options": [
                    {
                        "text": "Tempora voluptates distinctio facere ",
                        "_index": "book",
                        "_score": 1.0,
                        "_id": "1000087",
                        "_type": "book_document",
                        "_source": {
                            "description": null,
                            "summary": "Veniam dolores recusandae maxime laborum earum.",
                            "id": 1000087,
                            "state": "cancelled",
                            "authors": [
                                "Jayden van Luyssel",
                                "Yassin van Rooij",
                                "Florian van 't Erve",
                                "Mats van Nimwegen",
                                "Wessel Keltenie"
                            ],
                            "title": "Tempora voluptates distinctio facere."
                        }
                    },
                    {
                        "text": "Tempore sapiente repellat alias ad corrupti",
                        "_index": "book",
                        "_score": 1.0,
                        "_id": "29",
                        "_type": "book_document"
                        "_source": {
                            "description": null,
                            "summary": "Dolores minus architecto iure fugit qui sed.",
                            "id": 29,
                            "state": "canelled",
                            "authors": [
                                "Wout van Northeim",
                                "Lenn van Vliet-Kuijpers",
                                "Tijs Mulder"
                            ],
                            "title": "Tempore sapiente repellat alias ad."
                        },

                    },
                    {
                        "text": "Temporibus exercitationem minus expedita",
                        "_index": "book",
                        "_score": 1.0,
                        "_id": "17",
                        "_type": "book_document",
                        "_source": {
                            "description": null,
                            "summary": "A laborum alias voluptates tenetur sapiente modi.",
                            "id": 17,
                            "state": "canelled",
                            "authors": [
                                "Juliette Estey",
                                "Keano de Keijzer",
                                "Koen Scheffers",
                                "Florian van 't Erve",
                                "Tara Oversteeg",
                                "Mats van Nimwegen"
                            ],
                            "title": "Temporibus exercitationem minus expedita."
                        }
                    }
                ],
                "offset": 0
            }
        ]
    }

Term
++++

**Request**

.. code-block:: text

    GET http://127.0.0.1:8000/search/books/suggest/?summary_suggest__term=tovse

**Response**

.. code-block:: javascript

    {
        "_shards": {
            "failed": 0,
            "total": 1,
            "successful": 1
        },
        "summary_suggest__term": [
            {
                "text": "tovs",
                "offset": 0,
                "options": [
                    {
                        "text": "tove",
                        "score": 0.75,
                        "freq": 1
                    },
                    {
                        "text": "took",
                        "score": 0.5,
                        "freq": 1
                    },
                    {
                        "text": "twas",
                        "score": 0.5,
                        "freq": 1
                    }
                ],
                "length": 5
            }
        ]
    }

Phrase
++++++

**Request**

.. code-block:: text

    GET http://127.0.0.1:8000/search/books/suggest/?summary_suggest__phrase=slith%20tovs

**Response**

.. code-block:: javascript

    {
        "summary_suggest__phrase": [
            {
                "text": "slith tovs",
                "offset": 0,
                "options": [
                    {
                        "text": "slithi tov",
                        "score": 0.00083028956
                    }
                ],
                "length": 10
            }
        ],
        "_shards": {
            "failed": 0,
            "total": 1,
            "successful": 1
        }
    }

Functional suggestions
----------------------
If native suggestions are not good enough for you, use functional suggesters.

Configuration is very similar to native suggesters.

Document definition
~~~~~~~~~~~~~~~~~~~
Obviously, different filters require different approaches. For instance,
when using functional completion prefix filter, the best approach is to use
keyword field of the Elasticsearch. While for match completion, Ngram fields
work really well.

The following example indicates Ngram analyzer/filter usage.

*search_indexes/documents/book.py*

.. code-block:: python

    from django.conf import settings
    from django_elasticsearch_dsl import Document, Index, fields

    from elasticsearch_dsl import analyzer
    from elasticsearch_dsl.analysis import token_filter

    from books.models import Book

    edge_ngram_completion_filter = token_filter(
        'edge_ngram_completion_filter',
        type="edge_ngram",
        min_gram=1,
        max_gram=20
    )


    edge_ngram_completion = analyzer(
        "edge_ngram_completion",
        tokenizer="standard",
        filter=["lowercase", edge_ngram_completion_filter]
    )

    INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

    # See Elasticsearch Indices API reference for available settings
    INDEX.settings(
        number_of_shards=1,
        number_of_replicas=1
    )

    @INDEX.doc_type
    class BookDocument(Document):
        """Book Elasticsearch document."""

        # In different parts of the code different fields are used. There are
        # a couple of use cases: (1) more-like-this functionality, where `title`,
        # `description` and `summary` fields are used, (2) search and filtering
        # functionality where all of the fields are used.

        # ID
        id = fields.IntegerField(attr='id')

        # ********************************************************************
        # *********************** Main data fields for search ****************
        # ********************************************************************

        title = StringField(
            analyzer=html_strip,
            fields={
                'raw': KeywordField(),
                'suggest': fields.CompletionField(),
                'edge_ngram_completion': StringField(
                    analyzer=edge_ngram_completion
                ),
            }
        )

        # ...

        class Meta(object):
            """Meta options."""

            model = Book  # The model associate with this Document

ViewSet definition
~~~~~~~~~~~~~~~~~~

.. note:: The suggester filter backends shall come as last ones.

Functional suggesters for the view are configured in
``functional_suggester_fields`` property.

In the example below, the ``title_suggest`` is the name of the GET query
param which points to the ``title.raw`` field of the ``BookDocument`` document.
For the ``title_suggest`` the allowed suggester is
``FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX``. For Ngram match we have the
``title_suggest_match`` field, which points to ``title.edge_ngram_completion``
field of the same document. For ``title_suggest_match`` the allowed suggester
is ``FUNCTIONAL_SUGGESTER_COMPLETION_MATCH``.

URL shall be constructed in the following way:

.. code-block:: text

    /search/books/functional_suggest/?{QUERY_PARAM}__{SUGGESTER_NAME}={VALUE}

Example for ``completion_prefix`` suggester:

.. code-block:: text

    GET http://localhost:8000/search/books/functional_suggest/?title_suggest_prefix__completion_prefix=Temp

However, since we have ``default_suggester`` defined we can skip the
``__{SUGGESTER_NAME}`` part (if we want ``completion_prefix`` suggester
functionality). Thus, it might be written as short as:

.. code-block:: text

    GET http://localhost:8000/search/books/functional_suggest/?title_suggest_prefix=Temp

Example for ``completion_match`` suggester:

.. code-block:: text

    GET http://localhost:8000/search/books/functional_suggest/?title_suggest_match__completion_match=Temp

However, since we have ``default_suggester`` defined we can skip the
``__{SUGGESTER_NAME}`` part (if we want ``completion_match`` suggester
functionality). Thus, it might be written as short as:

.. code-block:: text

    GET http://localhost:8000/search/books/functional_suggest/?title_suggest_match=Temp

*search_indexes/viewsets/book.py*


.. code-block:: python

    from django_elasticsearch_dsl_drf.constants import (
        # ...
        FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
        FUNCTIONAL_SUGGESTER_COMPLETION_MATCH,
    )
    from django_elasticsearch_dsl_drf.filter_backends import (
        # ...
        SuggesterFilterBackend,
    )

    class BookDocumentViewSet(DocumentViewSet):
        """The BookDocument view."""

        document = BookDocument
        serializer_class = BookDocumentSerializer
        lookup_field = 'id'
        filter_backends = [
            FilteringFilterBackend,
            IdsFilterBackend,
            OrderingFilterBackend,
            DefaultOrderingFilterBackend,
            SearchFilterBackend,
            FacetedSearchFilterBackend,
            HighlightBackend,
            FunctionalSuggesterFilterBackend,  # This should come as last
        ]

        # ...

        # Functional suggester fields
        functional_suggester_fields = {
            'title_suggest': {
                'field': 'title.raw',
                'suggesters': [
                    FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
                ],
                'default_suggester': FUNCTIONAL_SUGGESTER_COMPLETION_PREFIX,
                'options': {
                    'size': 25,
                    'from': 0,
                }
            },
            'title_suggest_match': {
                'field': 'title.edge_ngram_completion',
                'suggesters': [FUNCTIONAL_SUGGESTER_COMPLETION_MATCH],
                'default_suggester': FUNCTIONAL_SUGGESTER_COMPLETION_MATCH,
            }
        }

.. note::

    Note, that in ``functional_suggester_fields['title_suggest']['options']``
    there are two params: ``size`` and ``from``. They control the query size
    and the offset of the generated functional suggest query.

Highlighting
------------
Highlighters enable you to get highlighted snippets from one or more fields
in your search results so you can show users where the query matches are.

**ViewSet definition**

.. code-block:: python

    from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
    from django_elasticsearch_dsl_drf.filter_backends import (
        # ...
        HighlightBackend,
    )

    from ..documents import BookDocument
    from ..serializers import BookDocumentSimpleSerializer


    class BookDocumentViewSet(BaseDocumentViewSet):
    """The BookDocument view."""

        document = BookDocument
        # serializer_class = BookDocumentSerializer
        serializer_class = BookDocumentSimpleSerializer
        lookup_field = 'id'
        filter_backends = [
            # ...
            HighlightBackend,
        ]

        # ...

        # Define highlight fields
        highlight_fields = {
            'title': {
                'enabled': True,
                'options': {
                    'pre_tags': ["<b>"],
                    'post_tags': ["</b>"],
                }
            },
            'summary': {
                'options': {
                    'fragment_size': 50,
                    'number_of_fragments': 3
                }
            },
            'description': {},
        }

        # ...

**Request**

.. code-block:: text

    GET http://127.0.0.1:8000/search/books/?search=optimisation&highlight=title&highlight=summary

**Response**

.. code-block:: javascript

    {
        "count": 1,
        "next": null,
        "previous": null,
        "facets": {
            "_filter_publisher": {
                "publisher": {
                    "buckets": [
                        {
                            "key": "Self published",
                            "doc_count": 1
                        }
                    ],
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 0
                },
                "doc_count": 1
            }
        },
        "results": [
            {
                "id": 999999,
                "title": "Performance optimisation",
                "description": null,
                "summary": "Ad animi adipisci libero facilis iure totam
                            impedit. Facilis maiores quae qui magnam dolores.
                            Veritatis quia amet porro voluptates iure quod
                            impedit. Dolor voluptatibus maiores at libero
                            magnam.",
                "authors": [
                    "Artur Barseghyan"
                ],
                "publisher": "Self published",
                "publication_date": "1981-04-29",
                "state": "cancelled",
                "isbn": "978-1-7372176-0-2",
                "price": 40.51,
                "pages": 162,
                "stock_count": 30,
                "tags": [
                    "Guide",
                    "Poetry",
                    "Fantasy"
                ],
                "highlight": {
                    "title": [
                        "Performance <b>optimisation</b>"
                    ]
                },
                "null_field": null
            }
        ]
    }

Pagination
----------

Page number pagination
~~~~~~~~~~~~~~~~~~~~~~

By default, the ``PageNumberPagination`` class is used on all view sets
which inherit from ``DocumentViewSet``.

Example:

.. code-block:: text

    http://127.0.0.1:8000/search/books/?page=4
    http://127.0.0.1:8000/search/books/?page=4&page_size=100

Limit/offset pagination
~~~~~~~~~~~~~~~~~~~~~~~

In order to use a different ``pagination_class``, for instance the
``LimitOffsetPagination``, specify it explicitly in the view.

*search_indexes/viewsets/book.py*

.. code-block:: python

    # ...

    from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination

    # ...

    class BookDocumentView(DocumentViewSet):
        """The BookDocument view."""

        # ...

        pagination_class = LimitOffsetPagination

        # ...

Example:

.. code-block:: text

    http://127.0.0.1:8000/search/books/?limit=100
    http://127.0.0.1:8000/search/books/?offset=400&limit=100

Customisations
~~~~~~~~~~~~~~

If you want to add additional data to the paginated response, for instance,
the page size, subclass the correspondent pagination class and add your
modifications in the ``get_paginated_response_context`` method as follows:

.. code-block:: python

    from django_elasticsearch_dsl_drf.pagination import PageNumberPagination


    class CustomPageNumberPagination(PageNumberPagination):
        """Custom page number pagination."""

        def get_paginated_response_context(self, data):
            __data = super(
                CustomPageNumberPagination,
                self
            ).get_paginated_response_context(data)
            __data.append(
                ('current_page', int(self.request.query_params.get('page', 1)))
            )
            __data.append(
                ('page_size', self.get_page_size(self.request))
            )

            return sorted(__data)

Same applies to the customisations of the ``LimitOffsetPagination``.
