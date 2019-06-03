Dependencies
============
**elasticsearch and elasticsearch-dsl**

Depending on your Elasticsearch version (either 2.x, 5.x or 6.x) you should
use 2.x, 5.x or 6.x versions of the ``elasticsearch`` and ``elasticsearch-dsl``
packages accordingly.

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
+---------------+-------------------+---------------------------

As of 2019-05-30, latest versions of ``elasticsearch`` and ``elasticsearch-dsl``
do not work well together with ``django-elasticsearch-dsl`` (for which the
latter is to "blame").

**djangorestframework**

Initial version of this package was written for `djangorestframework
<https://pypi.python.org/pypi/djangorestframework>`_ 3.6.2.

Tested with the following versions of Django/Django REST Framework:

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
