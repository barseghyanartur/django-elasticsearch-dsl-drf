===========
Quick start
===========

Perhaps the best way to get acquainted with ``django-elasticsearch-dsl-drf``
is quick start tutorial.

See it as a guide of diving into integration of Elasticsearch with Django
with very low knowledge entry level.

Installation
============

(1) Install latest stable version from PyPI:

    .. code-block:: sh

        pip install django-elasticsearch-dsl-drf

(2) Add ``rest_framework``, ``django_elasticsearch_dsl`` and
    ``django_elasticsearch_dsl_drf`` to ``INSTALLED_APPS``:

    .. code-block:: python

        INSTALLED_APPS = (
            # ...
            # REST framework
            'rest_framework',

            # Django Elasticsearch integration
            'django_elasticsearch_dsl',

            # Django REST framework Elasticsearch integration (this package)
            'django_elasticsearch_dsl_drf',
            # ...
        )

(3) Basic Django REST framework and ``django-elasticsearch-dsl`` configuration:

    .. code-block:: python

        REST_FRAMEWORK = {
            'DEFAULT_AUTHENTICATION_CLASSES': (
                'rest_framework.authentication.BasicAuthentication',
                'rest_framework.authentication.SessionAuthentication',
            ),
            'DEFAULT_PAGINATION_CLASS':
                'rest_framework.pagination.PageNumberPagination',
            'PAGE_SIZE': 100,
            'ORDERING_PARAM': 'ordering',
        }

        # Elasticsearch configuration
        ELASTICSEARCH_DSL = {
            'default': {
                'hosts': 'localhost:9200'
            },
        }


Example app
===========

To get started, let's imagine we have a simple book register with a couple of
models.

- `Publisher model`_: The book publisher model. Each book might have only one
  publisher (``ForeignKey`` relation).
- `Author model`_: The book author model. Each book might have unlimited number
  of authors (``ManyToMany`` relation).
- `Tag model`_: The tag model. Each book might have unlimited number of
  tags (``ManyToMany`` relation).
- `Book model`_: The book model.

To keep things separate, our Django models will reside in the ``books`` app.
Elasticsearch documents and Django REST framework views will be defined in a
``search_indexes`` app. Both of the apps should be added to the
``INSTALLED_APPS``.

.. code-block:: python

    INSTALLED_APPS = (
        # ...
        'books',  # Books application
        'search_indexes',  # Elasticsearch integration with the Django
                           # REST framework
        # ...
    )

Sample models
-------------

Content of the ``books/models.py`` file. Additionally, see the code comments.

Required imports
~~~~~~~~~~~~~~~~
Imports required for model definition.

.. code-block:: python

    import json

    from django.conf import settings
    from django.db import models
    from django.utils.translation import ugettext, ugettext_lazy as _

    from six import python_2_unicode_compatible

Book statuses
~~~~~~~~~~~~~

.. code-block:: python

    # States indicate the publishing status of the book. Publishing might
    # be in-progress, not yet published, published, rejected, etc.
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

Publisher model
~~~~~~~~~~~~~~~

.. code-block:: python

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

Author model
~~~~~~~~~~~~

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

Tag model
~~~~~~~~~

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

Book model
~~~~~~~~~~

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

        # The only publisher information we're going to need in our document
        # is the publisher name. Since publisher isn't a required field,
        # we define a properly on a model level to avoid indexing errors on
        # non-existing relation.
        @property
        def publisher_indexing(self):
            """Publisher for indexing.

            Used in Elasticsearch indexing.
            """
            if self.publisher is not None:
                return self.publisher.name

        # As of tags, again, we only need a flat list of tag names, on which
        # we can filter. Therefore, we define a properly on a model level,
        # which will return a JSON dumped list of tags relevant to the
        # current book model object.
        @property
        def tags_indexing(self):
            """Tags for indexing.

            Used in Elasticsearch indexing.
            """
            return json.dumps([tag.title for tag in self.tags.all()])

Admin classes
-------------

This is just trivial. A couple of correspondent admin classes in order to
ba able to fill some data.

.. code-block:: python

    from django.contrib import admin

    from .models import *


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

Create database tables
----------------------

For now, just run the migrations to create the database tables.

.. code-block:: sh

    ./manage.py makemigrations books
    ./manage.py migrate books

Fill in some data
-----------------

If you have followed the instructions, you should now be able to log into the
Django admin and create a dozen of Book/Author/Publisher/Tag records in admin.

- http://localhost:8000/admin/books/publisher/
- http://localhost:8000/admin/books/author/
- http://localhost:8000/admin/books/tag/
- http://localhost:8000/admin/books/book/

Once you've done that, proceed to the next step.

Sample document
---------------

In Elasticsearch, a document is a basic unit of information that can be
indexed. For example, you can have a document for a single customer, another
document for a single product, and yet another for a single order. This
document is expressed in JSON (JavaScript Object Notation) which is an
ubiquitous internet data interchange format.

Within an index/type, you can store as many documents as you want. Note that
although a document physically resides in an index, a document actually must
be indexed/assigned to a type inside an index.

Simply said, Document in Elasticsearch is similar to Model in Django.

Often, complicated SQL model structures are flatterned in Elasticsearch
indexes. Complicated relations are denormalized.

In our example, all 4 models (``Author``, ``Publisher``, ``Tag``, ``Book``)
would be flatterned into a single ``BookDocument``, which would hold all
the required information.

Content of the ``search_indexes/documents/book.py`` file. Additionally, see
the code comments.

Required imports
~~~~~~~~~~~~~~~~

.. code-block:: python

    from django_elasticsearch_dsl import DocType, Index, fields
    from elasticsearch_dsl import analyzer

    from books.models import Book

Index definition
~~~~~~~~~~~~~~~~

.. code-block:: python

    # Name of the Elasticsearch index
    BOOK_INDEX = Index('book')
    # See Elasticsearch Indices API reference for available settings
    BOOK_INDEX.settings(
        number_of_shards=1,
        number_of_replicas=1
    )

Custom analyzers
~~~~~~~~~~~~~~~~

.. code-block:: python

    html_strip = analyzer(
        'html_strip',
        tokenizer="standard",
        filter=["standard", "lowercase", "stop", "snowball"],
        char_filter=["html_strip"]
    )

Document definition
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    @BOOK_INDEX.doc_type
    class BookDocument(DocType):
        """Book Elasticsearch document."""

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

Syncing Django's database with Elasticsearch indexes
----------------------------------------------------

So far, we have a couple of Django models and a single (decentralized)
Elasticsearch index/document (Book).

The excellent ``django-elasticsearch-dsl`` library makes a good job of keeping
the Book index fresh. It makes use of signals, so whenever the Book model
is changed, the correspondent BookDocument indexes would be updated.

To simply run the full sync between Django's database and Elasticsearch, do
as follows:

(1) Create Elasticsearch indexes:

    .. code-block:: sh

        ./manage.py search_index --create -f

(2) Sync the data:

    .. code-block:: sh

        ./manage.py search_index --populate -f

However, in case if a Tag, Publisher or Author models change, the Book index
would not be automatically updated.

In order to keep indexes fresh, you will have to write a couple of simple
lines of code (using Django's signals). Whenever a change is made to any
of the Tag, Publisher or Author models, we're going to update the correspondent
BookDocument index.

Sample serializer
-----------------

At this step we're going to define a serializer to be used in the
Django REST framework ViewSet.

Content of the ``search_indexes/serializers.py`` file. Additionally, see
the code comments.

Required imports
~~~~~~~~~~~~~~~~

.. code-block:: python

    import json

    from rest_framework import serializers
    from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

    from .documents import BookDocument


Serializer definition
~~~~~~~~~~~~~~~~~~~~~

Simplest way to create a serializer, is to just specify which fields are
needed to be serialized and leave it further to the dynamic serializer.

.. code-block:: python

    class BookDocumentSerializer(DocumentSerializer):
        """Serializer for the Book document."""

        tags = serializers.SerializerMethodField()

        class Meta(object):
            """Meta options."""

            # Specify the correspondent document class
            document = BookDocument

            # List the serializer fields. Note, that the order of the fields
            # is preserved in the ViewSet.
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

        def get_tags(self, obj):
            """Get tags."""
            return json.loads(obj.tags)

However, if dynamic serializer doesn't work for your or you want to customize
too many things, you are free to use standard ``Serializer`` class of the
Django REST framework.

.. code-block:: python

    class BookDocumentSerializer(serializers.Serializer):
        """Serializer for the Book document."""

        id = serializers.IntegerField(read_only=True)

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

            # List the serializer fields. Note, that the order of the fields
            # is preserved in the ViewSet.
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

        def get_tags(self, obj):
            """Get tags."""
            return json.loads(obj.tags)

ViewSet definition
------------------

At this step, we're going to define Django REST framework ViewSets.

