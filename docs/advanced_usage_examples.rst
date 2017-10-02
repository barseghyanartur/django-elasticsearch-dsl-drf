=======================
Advanced usage examples
=======================

Advanced Django REST framework integration examples.

See the `example project
<https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/tree/master/examples/simple>`_
for sample models/views/serializers.

- `models
  <https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/blob/master/examples/simple/books/models.py>`_
- `documents
  <https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/blob/master/examples/simple/search_indexes/documents/book.py>`_
- `serializers
  <https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/blob/master/examples/simple/search_indexes/serializers.py>`_
- `views
  <https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/blob/master/examples/simple/search_indexes/views.py>`_

Contents:

.. contents:: Table of Contents

Example app
===========

Sample models
-------------

*books/models.py*

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


    class Tag(models.Model):
        """Simple tag model."""

        title = models.CharField(max_length=255, unique=True)

        class Meta(object):
            """Meta options."""

            verbose_name = _("Tag")
            verbose_name_plural = _("Tags")

        def __str__(self):
            return self.title


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
    from django_elasticsearch_dsl import DocType, Index, fields
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
    class BookDocument(DocType):
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

            model = Book  # The model associate with this DocType

Sample serializer
-----------------

*search_indexes/serializers.py*

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

*search_indexes/viewsets.py*

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
    from django_elasticsearch_dsl_drf.views import BaseDocumentViewSet

    # Example app models
    from search_indexes.documents.book import BookDocument
    from search_indxes.serializers import BookDocumentSerializer


    class BookDocumentView(BaseDocumentViewSet):
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
            'description',
            'summary',
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

Search in all fields (``title``, ``description`` and ``summary``) for word
"education".

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=education

**Search a single term on specific field**

In order to search in specific field (``title``) for term "education", add
the field name separated with ``|`` to the search term.

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=title|education

**Search for multiple terms**

In order to search for multiple terms "education", "technology" add
multiple ``search`` query params.

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=education&search=technology

**Search for multiple terms on specific fields**

In order to search for multiple terms "education", "technology" in specific
fields add multiple ``search`` query params and field names separated with
``|`` to each of the search terms.

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=title|education&search=summary|technology

Filtering
^^^^^^^^^

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

    http://127.0.0.1:8080/search/books/?state__in=published|in_progress

**Filter document by a single field**

Filter documents by (field ``tag``) "education".

.. code-block:: text

    http://127.0.0.1:8080/search/books/?tag=education

**Filter documents by multiple fields**

Filter documents by multiple fields (field ``tags``) "education" and "economy"
with use of functional ``in`` query filter.

.. code-block:: text

    http://127.0.0.1:8080/search/books/?tags__in=education|economy

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
^^^^^^^^

The ``-`` prefix means ordering should be descending.

**Order documents by field (ascending)**

Order documents by field ``price`` (ascending).

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=title|lorem&ordering=price

**Order documents by field (descending)**

Order documents by field ``price`` (descending).

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=title|lorem&ordering=-price

**Order documents by multiple fields**

If you want to order by multiple fields, use multiple ordering query params. In
the example below, documents would be ordered first by field
``publication_date`` (descending), then by field ``price`` (ascending).

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=title|lorem&ordering=-publication_date&ordering=price

Ids filter
----------
Filters documents that only have the provided ids.

.. code-block:: text

    http://127.0.0.1:8000/api/articles/?ids=68|64|58

Or, alternatively:

.. code-block:: text

    http://127.0.0.1:8000/api/articles/?ids=68&ids=64&ids=58

Faceted search
--------------

In order to add faceted search support, we would have to extend our
view set in the following way:

*search_indexes/viewsets.py*

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

    class BookDocumentView(BaseDocumentViewSet):
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

    http://localhost:8000/search/publishers/?location__geo_distance=100000km|12.04|-63.93

**Geo-polygon filtering**

Filter documents that are located in the given polygon.

.. code-block:: text

    http://localhost:8000/search/publishers/?location__geo_polygon=40,-70|30,-80|20,-90

**Geo-bounding-box filtering**

Filter documents that are located in the given bounding box.

.. code-block:: text

    http://localhost:8000/search/publishers/?location__geo_bounding_box=44.87,40.07|43.87,41.11

Ordering
~~~~~~~~

**Geo-distance ordering**

.. code-block:: text

    http://localhost:8000/search/publishers/?ordering=location|48.85|2.30|km|plane

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

    from django_elasticsearch_dsl import DocType, Index, fields

    from books.models import Publisher

    # Name of the Elasticsearch index
    INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

    # See Elasticsearch Indices API reference for available settings
    INDEX.settings(
        number_of_shards=1,
        number_of_replicas=1
    )


    @INDEX.doc_type
    class PublisherDocument(DocType):
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

            model = Publisher  # The model associate with this DocType

After that the ``name.suggest``, ``city.suggest``, ``state_province.suggest``
and ``country.suggest`` fields would be available for suggestions feature.

Serializer definition
^^^^^^^^^^^^^^^^^^^^^

This is how publisher serializer would look like.

*search_indexes/serializers.py*

.. code-block:: python

    import json

    from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

    class PublisherDocumentSerializer(DocumentSerializer):
        """Serializer for Publisher document."""

        location = serializers.SerializerMethodField()

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

        def get_location(self, obj):
        """Represent location value."""
        try:
            return obj.location.to_dict()
        except:
            return {}

ViewSet definition
^^^^^^^^^^^^^^^^^^

In order to add suggestions support, we would have to extend our view set in
the following way:

*search_indexes/viewsets.py*

.. code-block:: python

    # ...

    from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
    from django_elasticsearch_dsl_drf.filter_backends import (
        # ...
        SuggesterFilterBackend,
    )

    # ...

    class PublisherDocumentViewSet(BaseDocumentViewSet):
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
        "country_suggest__completion": [
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

Term and Phrase suggestions
~~~~~~~~~~~~~~~~~~~~~~~~~~~
While for the ``completion`` suggesters to work the ``CompletionField`` shall
be used, the ``term`` and ``phrase`` suggesters work on common text fields.

Document definition
^^^^^^^^^^^^^^^^^^^

*search_indexes/documents/book.py*

.. code-block:: python

    from django.conf import settings

    from django_elasticsearch_dsl import DocType, Index, fields

    from books.models import Book

    # Name of the Elasticsearch index
    INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

    # See Elasticsearch Indices API reference for available settings
    INDEX.settings(
        number_of_shards=1,
        number_of_replicas=1
    )

    @INDEX.doc_type
    class BookDocument(DocType):
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

            model = Book  # The model associate with this DocType

ViewSet definition
^^^^^^^^^^^^^^^^^^

*search_indexes/viewsets.py*

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
        SUGGESTER_PHRASE,
        SUGGESTER_TERM,
    )
    from django_elasticsearch_dsl_drf.filter_backends import (
        # ...
        SuggesterFilterBackend,
    )

    class BookDocumentViewSet(BaseDocumentViewSet):
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
            SuggesterFilterBackend,
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
            'title_suggest': 'title.suggest',
            'publisher_suggest': 'publisher.suggest',
            'tag_suggest': 'tags.suggest',
            'summary_suggest': 'summary',
        }

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

Pagination
----------

Page number pagination
~~~~~~~~~~~~~~~~~~~~~~

By default, the ``PageNumberPagination`` class is used on all view sets
which inherit from ``BaseDocumentViewSet``.

Example:

.. code-block:: text

    http://127.0.0.1:8000/search/books/?page=4
    http://127.0.0.1:8000/search/books/?page=4&page_size=100

Limit/offset pagination
~~~~~~~~~~~~~~~~~~~~~~~

In order to use a different ``pagination_class``, for instance the
``LimitOffsetPagination``, specify it explicitly in the view.

*search_indexes/viewsets.py*

.. code-block:: python

    # ...

    from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination

    # ...

    class BookDocumentView(BaseDocumentViewSet):
        """The BookDocument view."""

        # ...

        pagination_class = LimitOffsetPagination

        # ...

Example:

.. code-block:: text

    http://127.0.0.1:8000/search/books/?limit=100
    http://127.0.0.1:8000/search/books/?offset=400&limit=100
