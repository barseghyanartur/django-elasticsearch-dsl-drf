============================
django-elasticsearch-dsl-drf
============================
Integrate `django-elasticsearch-dsl
<https://pypi.python.org/pypi/django-elasticsearch-dsl>`_ with
`Django REST framework <https://pypi.python.org/pypi/djangorestframework>`_ in
the shortest way possible, with least efforts possible.

Package provides views, serializers, filter backends and other handy tools.

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

    or latest stable version from GitHub:

    .. code-block:: sh

        pip install https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/archive/stable.tar.gz

(2) Add ``rest_framework``, ``django_elasticsearch_dsl`` and
    ``django_elasticsearch_dsl_drf`` to ``INSTALLED_APPS``:

    .. code-block:: python

        INSTALLED_APPS = (
            # ...
            'rest_framework',  # REST framework
            'django_elasticsearch_dsl',  # Elasticsearch integration
            'django_elasticsearch_dsl_drf',  # This app
            # ...
        )


Search
======
Query param name reserved for search is ``search``. Make sure your models and
documents do not have it as a field or attribute.

Multiple search terms are joined with ``OR``.

Let's assume we have a number of Book items with fields ``title``,
``description`` and ``summary``.

Search in all fields
--------------------

Search in all fields (``name``, ``address``, ``city``, ``state_province`` and
``country``) for word "reilly".

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?search=reilly

Search a single term on specific field
--------------------------------------

In order to search in specific field (``name``) for term "reilly", add
the field name separated with ``|`` to the search term.

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?search=name|reilly

Search for multiple terms
-------------------------

In order to search for multiple terms "reilly", "bloomsbury" add
multiple ``search`` query params.

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?search=reilly&search=bloomsbury

Search for multiple terms in specific fields
--------------------------------------------

In order to search for multiple terms "reilly", "bloomsbury" in specific
fields add multiple ``search`` query params and field names separated with
``|`` to each of the search terms.

.. code-block:: text

    http://127.0.0.1:8080/search/publisher/?search=name|reilly&search=city|london

Filtering
=========

Supported lookups
-----------------

Native
~~~~~~

The following native (to Elasticsearch) filters/lookups are implemented:

- `term`_
- `terms`_
- `range`_
- `exists`_
- `prefix`_
- `wildcard`_
- `regexp`
- `fuzzy`
- `type`
- `ids`_

term
^^^^
Find documents which contain the exact term specified in the field specified.

.. code-block:: text

    http://127.0.0.1:8080/search/books/?tags__term=education&tags__term=economy

terms
^^^^^
Find documents which contain any of the exact terms specified in the field
specified.

range
^^^^^
Find documents where the field specified contains values (dates, numbers, or
strings) in the range specified.

exists
^^^^^^
Find documents where the field specified contains any non-null value.

prefix
^^^^^^
Find documents where the field specified contains terms which begin with the
exact prefix specified.

wildcard
^^^^^^^^
Find documents where the field specified contains terms which match the pattern
specified, where the pattern supports single character wildcards (?) and
multi-character wildcards (*)

ids
^^^
Find documents with the specified type and IDs.

Functional
~~~~~~~~~~

The following functional (non-native to Elasticsearch, but common in Django)
filters/lookups are implemented:

- `contains`_
- `in`_
- `gt`_
- `gte`_
- `lt`_
- `lte`_
- `startswith`_
- `endswith`_
- `isnull`_
- `exclude`_

contains
^^^^^^^^
Case-insensitive containment test.

in
^^
In a given list.

gt
^^
Greater than.

gte
^^^
Greater than or equal to.

lt
^^
Less than.

lte
^^^
Less than or equal to.

startswith
^^^^^^^^^^
Case-sensitive starts-with.

endswith
^^^^^^^^
Case-sensitive ends-with.

isnull
^^^^^^
Takes either True or False.

exclude
^^^^^^^
Returns a new query set of containing objects that do not match the given
lookup parameters.

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

Additionally, see:

- `Basic usage examples
  <https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/blob/master/docs/basic_usage_examples.rst>`_
- `Advanced usage examples
  <https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/blob/master/docs/advanced_usage_examples.rst>`_
- `Misc usage examples
  <https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/blob/master/docs/misc_usage_examples.rst>`_

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

    ./runtests.py src/django_elasticsearch_dsl_drf/tests/test_filtering.py

Or:

.. code-block:: sh

    ./manage.py test django_elasticsearch_dsl_drf.tests.test_ordering

It's assumed that you have all the requirements installed. If not, first
install the test requirements:

.. code-block:: sh

    pip install -r examples/requirements/test.txt

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
