Dependencies
============
**elasticsearch and elasticsearch-dsl**

Depending on your ``Elasticsearch`` version (either 2.x, 5.x, 6.x or 7.x) you
should use 2.x, 5.x, 6.x or 7.x versions of the ``elasticsearch`` and
``elasticsearch-dsl`` packages accordingly.

Current compatibility matrix is:

+--------------+---------------+
| This package | Elasticsearch |
+--------------+---------------+
| 0.18.x       | 2.x, 5.x, 6.x |
+--------------+---------------+
| 0.19.x       | 6.x           |
+--------------+---------------+
| 0.20.x       | 6.x, 7.x      |
+--------------+---------------+

**django-elasticsearch-dsl**

You are advised to use the latest version of `django-elasticsearch-dsl
<https://pypi.python.org/pypi/django-elasticsearch-dsl>`_.

The following versions have been tested and work well together:

+---------------+-------------------+--------------------------+
| elasticsearch | elasticsearch-dsl | django-elasticsearch-dsl |
+---------------+-------------------+--------------------------+
| 2.4.1         | 2.2.0             | 0.5.1                    |
+---------------+-------------------+--------------------------+
| 5.4.0         | 5.3.0             | 0.5.1                    |
+---------------+-------------------+--------------------------+
| 6.3.0         | 6.1.0             | 0.5.1                    |
+---------------+-------------------+--------------------------+
| 6.3.0         | 6.4.0             | 6.4.2                    |
+---------------+-------------------+--------------------------+
| 7.0.2         | 7.0.0             | 7.0.0                    |
+---------------+-------------------+--------------------------+

As of ``django-elasticsearch-dsl-drf`` 0.19, support for Elasticsearch versions
prior 6.x has been dropped.

**Django/ Django REST Framework**

Initial version of this package was written for `djangorestframework
<https://pypi.python.org/pypi/djangorestframework>`_ 3.6.2.

Starting from ``django-elasticsearch-dsl-drf`` version 0.18, support for
``Django`` versions prior 1.11 and ``Django REST Framework`` versions prior 3.9
has been dropped.

Current compatibility matrix is:

+--------+-----------------------+
| Django | Django REST Framework |
+--------+-----------------------+
| 1.11   | 3.9.3                 |
+--------+-----------------------+
| 2.0    | 3.9.3                 |
+--------+-----------------------+
| 2.1    | 3.9.3                 |
+--------+-----------------------+
| 2.2    | 3.9.3                 |
+--------+-----------------------+
| 3.0    | 3.11.0                |
+--------+-----------------------+

The version 0.17.7 has been tested with the following versions of
Django and Django REST Framework:

+--------+-----------------------+
| Django | Django REST Framework |
+--------+-----------------------+
| 1.8    | 3.6.2                 |
+--------+-----------------------+
| 1.9    | 3.6.2                 |
+--------+-----------------------+
| 1.10   | 3.6.2                 |
+--------+-----------------------+
| 1.11   | 3.7.7                 |
+--------+-----------------------+
| 2.0    | 3.7.7                 |
+--------+-----------------------+
| 2.1    | 3.8.2                 |
+--------+-----------------------+
| 2.2    | 3.9.2                 |
+--------+-----------------------+
