Dependencies
============
**elasticsearch and elasticsearch-dsl**

Depending on your ``Elasticsearch`` version (either 2.x, 5.x or 6.x) you should
use 2.x, 5.x or 6.x versions of the ``elasticsearch`` and ``elasticsearch-dsl``
packages accordingly.

**django-elasticsearch-dsl**

You are advised to use the latest version of `django-elasticsearch-dsl
<https://pypi.python.org/pypi/django-elasticsearch-dsl>`_.

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
