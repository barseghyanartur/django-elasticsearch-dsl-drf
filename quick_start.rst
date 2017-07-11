===========
Quick start
===========

The best way to get acquainted with ``django-elasticsearch-dsl-drf``.

See it as a guide of diving into integration of Elasticsearch with Django
with very low knowledge entry level.

Contents:

.. contents:: Table of Contents

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

.. code-block:: text

    http://localhost:8000/admin/books/publisher/
    http://localhost:8000/admin/books/author/
    http://localhost:8000/admin/books/tag/
    http://localhost:8000/admin/books/book/

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

Full database sync
~~~~~~~~~~~~~~~~~~

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

Sample partial sync (using custom signals)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to keep indexes fresh, you will have to write a couple of simple
lines of code (using Django's signals). Whenever a change is made to any
of the Tag, Publisher or Author models, we're going to update the correspondent
BookDocument index.

Required imports
^^^^^^^^^^^^^^^^

.. code-block:: python

    from django.db.models.signals import post_save, post_delete
    from django.dispatch import receiver

    from django_elasticsearch_dsl.registries import registry

Update book index on related model change
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    @receiver(post_save)
    def update_document(sender, **kwargs):
        """Update document on added/changed records.

        Update Book document index if related `books.Publisher` (`publisher`),
        `books.Author` (`authors`), `books.Tag` (`tags`) fields have been updated
        in the database.
        """
        app_label = sender._meta.app_label
        model_name = sender._meta.model_name
        instance = kwargs['instance']

        if app_label == 'book':
            # If it is `books.Publisher` that is being updated.
            if model_name == 'publisher':
                instances = instance.books.all()
                for _instance in instances:
                    registry.update(_instance)

            # If it is `books.Author` that is being updated.
            if model_name == 'author':
                instances = instance.books.all()
                for _instance in instances:
                    registry.update(_instance)

            # If it is `books.Tag` that is being updated.
            if model_name == 'tag':
                instances = instance.books.all()
                for _instance in instances:
                    registry.update(_instance)

Update book index on related model removal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    @receiver(post_delete)
    def delete_document(sender, **kwargs):
        """Update document on deleted records.

        Updates Book document from index if related `books.Publisher`
        (`publisher`), `books.Author` (`authors`), `books.Tag` (`tags`) fields
        have been removed from database.
        """
        app_label = sender._meta.app_label
        model_name = sender._meta.model_name
        instance = kwargs['instance']

        if app_label == 'books':
            # If it is `books.Publisher` that is being updated.
            if model_name == 'publisher':
                instances = instance.books.all()
                for _instance in instances:
                    registry.update(_instance)
                    # registry.delete(_instance, raise_on_error=False)

            # If it is `books.Author` that is being updated.
            if model_name == 'author':
                instances = instance.books.all()
                for _instance in instances:
                    registry.update(_instance)
                    # registry.delete(_instance, raise_on_error=False)

            # If it is `books.Tag` that is being updated.
            if model_name == 'tag':
                instances = instance.books.all()
                for _instance in instances:
                    registry.update(_instance)
                    # registry.delete(_instance, raise_on_error=False)

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


Content of the ``search_indexes/views.py`` file. Additionally, see
the code comments.

Required imports
~~~~~~~~~~~~~~~~

.. code-block:: python

    from django_elasticsearch_dsl_drf.constants import (
        LOOKUP_FILTER_TERMS,
        LOOKUP_FILTER_RANGE,
        LOOKUP_FILTER_PREFIX,
        LOOKUP_FILTER_WILDCARD,
        LOOKUP_QUERY_IN,
        LOOKUP_QUERY_GT,
        LOOKUP_QUERY_GTE,
        LOOKUP_QUERY_LT,
        LOOKUP_QUERY_LTE,
        LOOKUP_QUERY_EXCLUDE,
    )
    from django_elasticsearch_dsl_drf.filter_backends import (
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        SearchFilterBackend,
    )
    from django_elasticsearch_dsl_drf.views import BaseDocumentViewSet

    from .documents import BookDocument, PublisherDocument
    from .serializers import BookDocumentSerializer


ViewSet definition
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class BookDocumentView(BaseDocumentViewSet):
        """The BookDocument view."""

        document = BookDocument
        serializer_class = BookDocumentSerializer
        lookup_field = 'id'
        filter_backends = [
            FilteringFilterBackend,
            IdsFilterBackend,
            OrderingFilterBackend,
            SearchFilterBackend,
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
                # Note, that we limit the lookups of id field in this example,
                # to `range`, `in`, `gt`, `gte`, `lt` and `lte` filters.
                'lookups': [
                    LOOKUP_FILTER_RANGE,
                    LOOKUP_QUERY_IN,
                    LOOKUP_QUERY_GT,
                    LOOKUP_QUERY_GTE,
                    LOOKUP_QUERY_LT,
                    LOOKUP_QUERY_LTE,
                ],
            },
            'title': 'title.raw',
            'publisher': 'publisher.raw',
            'publication_date': 'publication_date',
            'state': 'state.raw',
            'isbn': 'isbn.raw',
            'price': {
                'field': 'price.raw',
                # Note, that we limit the lookups of `price` field in this
                # example, to `range`, `gt`, `gte`, `lt` and `lte` filters.
                'lookups': [
                    LOOKUP_FILTER_RANGE,
                    LOOKUP_QUERY_GT,
                    LOOKUP_QUERY_GTE,
                    LOOKUP_QUERY_LT,
                    LOOKUP_QUERY_LTE,
                ],
            },
            'pages': {
                'field': 'pages',
                # Note, that we limit the lookups of `pages` field in this
                # example, to `range`, `gt`, `gte`, `lt` and `lte` filters.
                'lookups': [
                    LOOKUP_FILTER_RANGE,
                    LOOKUP_QUERY_GT,
                    LOOKUP_QUERY_GTE,
                    LOOKUP_QUERY_LT,
                    LOOKUP_QUERY_LTE,
                ],
            },
            'stock_count': {
                'field': 'stock_count',
                # Note, that we limit the lookups of `stock_count` field in
                # this example, to `range`, `gt`, `gte`, `lt` and `lte`
                # filters.
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
                # Note, that we limit the lookups of `tags` field in
                # this example, to `terms, `prefix`, `wildcard`, `in` and
                # `exclude` filters.
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
                # Note, that we limit the lookups of `tags.raw` field in
                # this example, to `terms, `prefix`, `wildcard`, `in` and
                # `exclude` filters.
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
        ordering = ('id', 'title', 'price',)

URLs
----

At this step, we're going to define url patterns.

Content of the ``search_indexes/urls.py`` file. Additionally, see
the code comments.

Required imports
~~~~~~~~~~~~~~~~

.. code-block:: python

    from django.conf.urls import url, include
    from rest_framework_extensions.routers import ExtendedDefaultRouter

    from .views import BookDocumentView


Router definition
~~~~~~~~~~~~~~~~~

.. code-block:: python

    router = ExtendedDefaultRouter()
    books = router.register(r'books',
                            BookDocumentView,
                            base_name='bookdocument')

URL patterns
~~~~~~~~~~~~

.. code-block:: python

    urlpatterns = [
        url(r'^', include(router.urls)),
    ]

Check what you've done so far
-----------------------------

At this point, you are one step away from a working example of integrating
Elasticsearch DSL with Django.

URLs
~~~~

If you didn't add the urls of the ``search_indexes`` example application to
your project's global url patterns, make sure to do it now.

.. code-block:: python

    from django.conf.urls import include, url
    from search_indexes import urls as search_index_urls

    urlpatterns = [
        # ...
        # Search URLs
        url(r'^search/', include(search_index_urls)),
        # ...
    ]

Test in browser
~~~~~~~~~~~~~~~

Open the following URL in your browser.

.. code-block:: text

    http://localhost:8000/search/books/

Perform a number of lookups:

.. code-block:: text

    http://localhost:8001/search/books/?ids=54|55|56
    http://localhost:8001/search/books/?summary__contains=photography
    http://localhost:8001/search/books/?tags__contains=ython
    http://localhost:8001/search/books/?state=published
    http://localhost:8001/search/books/?pages__gt=10&pages__lt=30

Development and debugging
=========================

Looking for profiling tools for Elasticsearch?

Try `django-elasticsearch-debug-toolbar
<https://pypi.python.org/pypi/django-elasticsearch-debug-toolbar/>`_
package. It's implemented as a panel for the well known
`Django Debug Toolbar <https://pypi.python.org/pypi/django-debug-toolbar>`_
and gives you full insights on what's happening on the side of Elasticsearch.

Installation
------------

.. code-block:: sh

    pip install django-debug-toolbar
    pip install django-elasticsearch-debug-toolbar

Configuration
-------------

Change your development settings in the following way:

.. code-block:: python

    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'debug_toolbar_force.middleware.ForceDebugToolbarMiddleware',
    )

    INSTALLED_APPS += (
        'debug_toolbar',
        'elastic_panel',
    )

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

    DEBUG_TOOLBAR_PANELS = (
        # Defaults
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        # Additional
        'elastic_panel.panel.ElasticDebugPanel',
    )
