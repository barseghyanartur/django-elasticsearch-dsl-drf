factories
=========
Project dummy data (dynamic fixtures). Extremely useful if you want to test
your application on a large data set (which you don't have or difficult to
recreate each time for each developer).

Usage examples
--------------
**Create a single ``Book`` instance**

.. code-block:: python

    import factories

    book = factories.BookFactory()

**Create many (100) ``Book`` instances**

.. code-block:: python

    import factories

    book = factories.BookFactory.create_batch(100)

**Create a single ``Book`` instance with pre-defined attributes**

.. code-block:: python

    book = factories.BookFactory(
        title="My book title",
        publisher__country="AU",
    )
