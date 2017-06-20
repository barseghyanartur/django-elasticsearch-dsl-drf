============================
django-elasticsearch-dsl-drf
============================
Integrate `django-elasticsearch-dsl
<https://pypi.python.org/pypi/django-elasticsearch-dsl>`_ with
`Django REST framework <https://pypi.python.org/pypi/djangorestframework>`_ in
the shortest way possible, with least efforts possible.

Package provides views, filter backends and other handy tools.

You are expected to use `django-elasticsearch-dsl
<https://pypi.python.org/pypi/django-elasticsearch-dsl>`_ for defining your
document models.

Prerequisites
=============
- Django 1.8, 1.9, 1.10 and 1.11.
- Python 2.7, 3.4, 3.5, 3.6
- Elasticsearch 2.x, 5.x

Dependencies
============
- django-elasticsearch-dsl
- djangorestframework

Installation
============

(1) Install latest stable version from PyPI:

    .. code-block:: sh

        pip install django-elasticsearch-dsl-drf

    Or latest stable version from GitHub:

    .. code-block:: sh

        pip install https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/archive/stable.tar.gz

(2) Add ``rest_framework`` and ``django_elasticsearch_dsl`` to
    ``INSTALLED_APPS``:

    .. code-block:: python

        INSTALLED_APPS = (
            # ...
            'rest_framework',  # REST framework
            'django_elasticsearch_dsl',  # ElasticSearch integration
            # ...
        )

Usage examples
==============
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

Basic Django REST framework integration example
-----------------------------------------------
Sample basic example models
~~~~~~~~~~~~~~~~~~~~~~~~~~~

books/models.py:

.. code-block:: python

    class Publisher(models.Model):
        """Publisher."""

        name = models.CharField(max_length=30)
        address = models.CharField(max_length=50)
        city = models.CharField(max_length=60)
        state_province = models.CharField(max_length=30)
        country = models.CharField(max_length=50)
        website = models.URLField()

        class Meta(object):
            """Meta options."""

            ordering = ["id"]

        def __str__(self):
            return self.name


Sample basic example document
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

search_indexes/documents/publisher.py:

.. code-block:: python

    from django_elasticsearch_dsl import DocType, Index, fields
    from elasticsearch_dsl import analyzer

    from books.models import Publisher

    # Name of the ElasticSearch index
    PUBLISHER_INDEX = Index('publisher')
    # See ElasticSearch Indices API reference for available settings
    PUBLISHER_INDEX.settings(
        number_of_shards=1,
        number_of_replicas=1
    )


    @PUBLISHER_INDEX.doc_type
    class PublisherDocument(DocType):
        """Publisher ElasticSearch document."""

        id = fields.IntegerField(attr='id')

        name = fields.StringField(
            fields={
                'raw': fields.StringField(
                    analyzer='keyword'
                )
            }
        )
        address = fields.StringField(
            fields={
                'raw': fields.StringField(
                    analyzer='keyword'
                )
            }
        )
        city = fields.StringField(
            fields={
                'raw': fields.StringField(
                    analyzer='keyword'
                )
            }
        )
        state_province = fields.StringField(
            fields={
                'raw': fields.StringField(
                    analyzer='keyword'
                )
            }
        )
        country = fields.StringField(
            fields={
                'raw': fields.StringField(
                    analyzer='keyword'
                )
            }
        )
        website = fields.StringField(
            fields={
                'raw': fields.StringField(
                    analyzer='keyword'
                )
            }
        )

        class Meta(object):
            """Meta options."""

            model = Publisher  # The model associate with this DocType


Sample basic example serializer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

search_indexes/serializers.py:

.. code-block:: python

    import json

    from rest_framework import serializers

    class PublisherDocumentSerializer(serializers.Serializer):
        """Serializer for Publisher document."""

        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField(read_only=True)
        address = serializers.CharField(read_only=True)
        city = serializers.CharField(read_only=True)
        state_province = serializers.CharField(read_only=True)
        country = serializers.CharField(read_only=True)
        website = serializers.CharField(read_only=True)

        class Meta(object):
            """Meta options."""

            fields = read_only_fields = (
                'id',
                'name',
                'address',
                'city',
                'state_province',
                'country',
                'website',
            )
            read_only_fields = fields

Sample basic example view
~~~~~~~~~~~~~~~~~~~~~~~~~

search_indexes/views.py:

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
        SearchFilterBackend,
    )
    from django_elasticsearch_dsl_drf.views import BaseDocumentViewSet

    # Example app models
    from search_indexes.documents.publisher import PublisherDocument
    from search_indxes.serializers import PublisherDocumentSerializer

    class PublisherDocumentView(BaseDocumentViewSet):
        """The PublisherDocument view."""

        document = PublisherDocument
        serializer_class = PublisherDocumentSerializer
        lookup_field = 'id'
        filter_backends = [
            FilteringFilterBackend,
            OrderingFilterBackend,
            SearchFilterBackend,
        ]
        # Define search fields
        search_fields = (
            'name',
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

Advanced Django REST framework integration example
--------------------------------------------------

Sample advanced example models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

books/models.py:

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
        address = models.CharField(max_length=50)
        city = models.CharField(max_length=60)
        state_province = models.CharField(max_length=30)
        country = models.CharField(max_length=50)
        website = models.URLField()

        class Meta(object):
            """Meta options."""

            ordering = ["id"]

        def __str__(self):
            return self.name


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

            Used in ElasticSearch indexing.
            """
            if self.publisher is not None:
                return self.publisher.name

        @property
        def tags_indexing(self):
            """Tags for indexing.

            Used in ElasticSearch indexing.
            """
            return json.dumps([tag.title for tag in self.tags.all()])

Sample advanced example document
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

search_indexes/documents/book.py:

.. code-block:: python

    from django_elasticsearch_dsl import DocType, Index, fields
    from elasticsearch_dsl import analyzer

    from books.models import Book

    # Name of the ElasticSearch index
    BOOK_INDEX = Index('book')
    # See ElasticSearch Indices API reference for available settings
    BOOK_INDEX.settings(
        number_of_shards=1,
        number_of_replicas=1
    )


    html_strip = analyzer(
        'html_strip',
        tokenizer="standard",
        filter=["standard", "lowercase", "stop", "snowball"],
        char_filter=["html_strip"]
    )


    @BOOK_INDEX.doc_type
    class BookDocument(DocType):
        """Book ElasticSearch document."""

        id = fields.IntegerField(attr='id')

        title = fields.StringField(
            analyzer=html_strip,
            fields={
                'raw': fields.StringField(
                    analyzer='keyword'
                )
            }
        )

        description = fields.StringField(
            analyzer=html_strip,
            fields={
                'raw': fields.StringField(
                    analyzer='keyword'
                )
            }
        )

        summary = fields.StringField(
            analyzer=html_strip,
            fields={
                'raw': fields.StringField(
                    analyzer='keyword'
                )
            }
        )

        publisher = fields.StringField(
            attr='publisher_indexing',
            analyzer=html_strip,
            fields={
                'raw': fields.StringField(
                    analyzer='keyword'
                )
            }
        )

        publication_date = fields.DateField()

        state = fields.StringField(
            analyzer=html_strip,
            fields={
                'raw': fields.StringField(
                    analyzer='keyword'
                )
            }
        )

        isbn = fields.StringField(
            analyzer=html_strip,
            fields={
                'raw': fields.StringField(
                    analyzer='keyword'
                )
            }
        )

        price = fields.FloatField()

        pages = fields.IntegerField()

        stock_count = fields.IntegerField()

        tags = fields.StringField(
            attr='tags_indexing',
            analyzer=html_strip,
            fields={
                'raw': fields.StringField(
                    analyzer='keyword',
                    multi=True
                )
            },
            multi=True
        )

        class Meta(object):
            """Meta options."""

            model = Book  # The model associate with this DocType

Sample advanced example serializer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

search_indexes/serializers.py:

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
            read_only_fields = (
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

        def get_tags(self, obj):
            """Get tags."""
            return json.loads(obj.tags)

Sample advanced example view
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

search_indexes/views.py:

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
            'publisher': {
                'field': 'publisher.raw',
            },
            'publication_date': 'publication_date',
            'isbn': {
                'field': 'isbn.raw',
            },
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

Usage
~~~~~
Considering samples above, you should be able to perform the search, sorting
and filtering actions described below.

Sample queries
^^^^^^^^^^^^^^
Search
++++++
Query param name reserved for search is `search`. Make sure your models and
documents do not have it as a field or attribute.

Multiple search terms are joined with `OR`.

Let's assume we have a number of Book items with fields `title`, `description`
and `summary`.

Search in all fields
********************
Search in all fields (`title`, `summary` and `content`) for word "education"

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=education

Search in specific field
************************
In order to search in specific field (`title`) for term "education", add
the field name separated with `|` to the search term.

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=title|education

Search for multiple terms
*************************
In order to search for multiple terms "education", "technology" add
multiple `search` query params.

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=education&search=technology

Search for multiple terms in specific fields
********************************************
In order to search for multiple terms "education", "technology" in specific
fields add multiple `search` query params and field names separated with `|`
to each of the search terms.

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=title|education&search=summary|technology

Filtering
+++++++++
Let's assume we have a number of Book documents with the tags (education,
politics, economy, biology, climate, environment, internet, technology).

Multiple filter terms are joined with `AND`.

Filter documents by state
*************************
Filter documents by `state` "published".

.. code-block:: text

    http://127.0.0.1:8080/search/books/?state=published

Filter documents by multiple states
***********************************
Filter documents by `states` "published" and "in_progress"

.. code-block:: text

    http://127.0.0.1:8080/search/books/?state__in=published|in_progress

Filter document by a single tag
*******************************
Filter documents by tag "education".

.. code-block:: text

    http://127.0.0.1:8080/search/books/?tag=education

Filter documents by multiple tags
*********************************
Filter documents by multiple tags (`tags`) "education" and "economy" with use of
functional `in` query filter.

.. code-block:: text

    http://127.0.0.1:8080/search/books/?tags__in=education|economy

You can achieve the same effect by specifying multiple tags (`tags`)
"education" and "economy". Note, that in this case multiple filter terms are
joined with `OR`.

.. code-block:: text

    http://127.0.0.1:8080/search/books/?tags=education&tags=economy

If you want the same as above, but joined with `AND`, add `__term` to each
lookup.

.. code-block:: text

    http://127.0.0.1:8080/search/books/?tags__term=education&tags__term=economy

Filter documents by a word part of a single tag
***********************************************
Filter documents by a part word part in single tag (`tags`). Word part should
match both "technology" and "biology".

.. code-block:: text

    http://127.0.0.1:8080/search/books/?tags__wildcard=*logy

Ordering
++++++++
The `-` prefix means ordering should be descending.

Order documents by field (ascending)
************************************
Filter documents by field `price` (ascending).

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=title|lorem&ordering=price

Order documents by field (descending)
*************************************
Filter documents by field `price` (descending).

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=title|lorem&ordering=-price

Order documents by multiple fields
**********************************
If you want to order by multiple fields, use multiple ordering query params. In
the example below, documents would be ordered first by field `publication_date`
(descending), then by field `price` (ascending).

.. code-block:: text

    http://127.0.0.1:8080/search/books/?search=title|lorem&ordering=-publication_date,ordering=price



Testing
=======
Project is covered with tests.

To test with all supported Python/Django versions type:

.. code-block:: sh

    tox

To test against specific environment, type:

.. code-block:: sh

    tox -e py36-django110

To test just your working environment type:

.. code-block:: sh

    ./runtests.py

To run a single test in your working environment type:

.. code-block:: sh

    ./runtests.py src/django_elasticsearch_dsl_drf/tests/test_ordering.py

Or:

.. code-block:: sh

    ./manage.py test django_elasticsearch_dsl_drf.tests.test_ordering

It's assumed that you have all the requirements installed. If not, first
install the test requirements:

.. code-block:: sh

    pip install -r examples/requirements/test.txt

Various handy helpers
---------------------
More like this
~~~~~~~~~~~~~~
To get more-like-this results on a random registered model, do as follows:

.. code-block:: python

    from django_elasticsearch_dsl_drf.helpers import more_like_this
    from books.models import Book
    book = Book.objects.first()
    similar_books = more_like_this(
        book,
        ['title', 'description', 'summary']
    )

Writing documentation
=====================
Keep the following hierarchy.

.. code-block:: text

    =====
    title
    =====

    header
    ======

    sub-header
    ----------

    sub-sub-header
    ~~~~~~~~~~~~~~

    sub-sub-sub-header
    ^^^^^^^^^^^^^^^^^^

    sub-sub-sub-sub-header
    ++++++++++++++++++++++

    sub-sub-sub-sub-sub-header
    **************************

License
=======
GPL 2.0/LGPL 2.1

Support
=======
For any issues contact me at the e-mail given in the `Author`_ section.

Author
======
Artur Barseghyan <artur.barseghyan@gmail.com>
