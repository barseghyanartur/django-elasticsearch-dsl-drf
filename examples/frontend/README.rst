==============================================
frontend demo for django-elasticsearch-dsl-drf
==============================================
Frontend demo for django-elasticsearch-dsl-drf

Quick start
===========
From the project root directory.

Install the django requirements
-------------------------------
Since project supports Django versions from 1.8 to 2.1, you may install
any version you want.

To install latest LTS version, do:

.. code-block:: sh

    pip install -r examples/requirements/django_1_11.txt

Install Elasticsearch requirements
----------------------------------
Since project supports Elasticsearch versions from 2.x to 6.x, you may install
any version you want.

To install requirements for 6.x, do:

.. code-block:: sh

    pip install examples/requirements/elastic_6x.txt

Run Elasticsearch
-----------------
It's really easy using Docker.

To run 6.3.2 using Docker, do:

.. code-block:: sh

    docker pull docker.elastic.co/elasticsearch/elasticsearch:6.3.2
    docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:6.3.2

Install React requirements
--------------------------
Note, that you should be using NodeJS > 7.5.

Typically, you would first do:

.. code-block:: sh

    nvm use 9

Then run the installer:

.. code-block:: sh

    ./scripts/yarn_install.sh

Run Django
----------
The following script would run the Django server which is used by the demo
app.

.. code-block:: sh

    ./scripts/runserver.sh

Run React demo app
------------------
Finally, run the React demo app:

.. code-block:: sh

    ./scripts/frontend.sh

Available Scripts
=================
In the project directory, you can run:

npm start
---------
Runs the app in the development mode.<br>
Open `http://localhost:3000 <http://localhost:3000>`_ to view it in the
browser.

.. code-block:: sh

    npm start

The page will reload if you make edits.<br>
You will also see any lint errors in the console.

npm test
--------
Launches the test runner in the interactive watch mode.<br>
See the section about `running tests
<https://facebook.github.io/create-react-app/docs/running-tests>`_ for more
information.

.. code-block:: sh

    npm test

npm run build
-------------
Builds the app for production to the `build` folder.
It correctly bundles React in production mode and optimizes the build for the
best performance.

.. code-block:: sh

    npm run build

The build is minified and the filenames include the hashes.<br>
Your app is ready to be deployed!

See the section about `deployment
<https://facebook.github.io/create-react-app/docs/deployment>`_ for more
information.

npm run eject
-------------

.. code-block:: sh

    npm run eject

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you
can `eject` at any time. This command will remove the single build dependency
from your project.

Instead, it will copy all the configuration files and the transitive
dependencies (Webpack, Babel, ESLint, etc) right into your project so you
have full control over them. All of the commands except `eject` will still
work, but they will point to the copied scripts so you can tweak them. At this
point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for
small and middle deployments, and you shouldn't feel obligated to use this
feature. However we understand that this tool wouldn't be useful if you
couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the `Create React App documentation
<https://facebook.github.io/create-react-app/docs/getting-started>`_.

To learn React, check out the `React documentation <https://reactjs.org/>`_.
