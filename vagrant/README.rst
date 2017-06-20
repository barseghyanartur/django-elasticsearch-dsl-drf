Vagrant
-------
Vagrant file for testing.

Versions
~~~~~~~~
- Java 8
- ElasticSearch 2.x

Installation
~~~~~~~~~~~~
Installing VirtualBox:

.. code-block:: sh

    sudo apt-get install virtualbox

Or on Mac Os:

.. code-block:: sh

    brew cask install virtualbox

Installing Vagrant:

.. code-block:: sh

    sudo apt-get install vagrant
    sudo apt-get install virtualbox-dkms

Or on Mac:

.. code-block:: sh

    brew cask install vagrant
    brew cask install vagrant-manager

Getting vagrant  machine up:

.. code-block:: sh

    vagrant box add precise32 http://files.vagrantup.com/precise32.box
    vagrant init precise32

Running a Vagrant environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To start up:

.. code-block:: sh

    vagrant up

To shut down:

.. code-block:: sh

    vagrant suspend

Browsing ElasticSearch indexes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A `head <https://github.com/mobz/elasticsearch-head>`_ plugin to browse
ElasticSearch indexes has been installed.

Just open the following link in your browser:

.. code-block:: text

    http://localhost:9200/_plugin/head/
