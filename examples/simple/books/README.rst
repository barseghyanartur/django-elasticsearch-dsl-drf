books
=====
Sample application.

Most of the code taken from `official Django documentation
<https://docs.djangoproject.com/en/1.8/topics/class-based-views/generic-display/#generic-views-of-objects>`_.

models
------
- Author
- Book
- Order
- OrderLine
- Publisher

management commands
-------------------
books_create_test_data
~~~~~~~~~~~~~~~~~~~~~~
Create project dummy data (dynamic fixtures). By default creates a 100 Book
records. Accepts an optional --number parameter for customising the number
of Book records created.

**Create Book records**

.. code-block:: sh

    ./manage.py books_create_test_data

**Create 1000 Book records**

.. code-block:: sh

    ./manage.py books_create_test_data --number=1000
