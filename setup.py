import os

from setuptools import find_packages, setup

version = '0.6.3'

DOCS_TRANSFORMATIONS = (
    (
        ':doc:`Dynamic serializer for Documents <basic_usage_examples>`',
        '`Dynamic serializer for Documents <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'basic_usage_examples.html#sample-serializer'
        '>`_'.format(version)
    ),
    (
        ':doc:`Search filter backend <advanced_usage_examples>`',
        '`Search filter backend <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'advanced_usage_examples.html#search'
        '>`_'.format(version)
    ),
    (
        ':doc:`Ordering filter backend <advanced_usage_examples>`',
        '`Ordering filter backend <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'advanced_usage_examples.html#ordering'
        '>`_'.format(version)
    ),
    (
        ':doc:`Filtering filter backend <advanced_usage_examples>`',
        '`Filtering filter backend <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'advanced_usage_examples.html#filtering'
        '>`_'.format(version)
    ),
    (
        ':doc:`Geo-spatial filtering filter backend <advanced_usage_examples>`',
        '`Geo-spatial filtering filter backend <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'advanced_usage_examples.html#geo-spatial-features'
        '>`_'.format(version)
    ),
    (
        ':doc:`Geo-spatial ordering filter backend <advanced_usage_examples>`',
        '`Geo-spatial ordering filter backend <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'advanced_usage_examples.html#geo-spatial-features'
        '>`_'.format(version)
    ),
    (
        ':doc:`Faceted search filter backend <advanced_usage_examples>`',
        '`Faceted search filter backend <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'advanced_usage_examples.html#faceted-search'
        '>`_'.format(version)
    ),
    (
        ':doc:`Highlight backend <advanced_usage_examples>`',
        '`Highlight backend <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'advanced_usage_examples.html#highlighting'
        '>`_'.format(version)
    ),
    (
        ':doc:`Pagination (Page number and limit/offset pagination) '
        '<advanced_usage_examples>`',
        '`Pagination (Page number and limit/offset pagination) <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'advanced_usage_examples.html#pagination'
        '>`_'.format(version)
    ),
    (
        ':doc:`quick start tutorial <quick_start>`',
        '`quick start tutorial <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'quick_start.html'
        '>`_'.format(version)
    ),
    (
        ':doc:`Suggester filter backend <advanced_usage_examples>`',
        '`Suggester filter backend <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'advanced_usage_examples.html#suggestions'
        '>`_'.format(version)
    ),
    (
        ':doc:`Ids filter backend <advanced_usage_examples>`',
        '`Ids filter backend <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'advanced_usage_examples.html#ids-filter'
        '>`_'.format(version)
    ),
)

try:
    readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
    for __search, __replace in DOCS_TRANSFORMATIONS:
        readme = readme.replace(__search, __replace)
except:
    readme = ''

install_requires = [
    'six>=1.9',
    'django-nine>=0.1.10',
    'django-elasticsearch-dsl>=0.3',
    'elasticsearch-dsl',
    'elasticsearch',
    'djangorestframework',
]

extras_require = []

tests_require = [
    'factory_boy',
    'fake-factory',
    'pytest',
    'pytest-django',
    'pytest-cov',
    'tox',
]

setup(
    name='django-elasticsearch-dsl-drf',
    version=version,
    description="Integrate Elasticsearch DSL with Django REST framework.",
    long_description=readme,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Environment :: Web Environment",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or "
        "later (LGPLv2+)",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    keywords="django, elasticsearch, elasticsearch-dsl, django rest framework",
    author='Artur Barseghyan',
    author_email='artur.barseghyan@gmail.com',
    url='https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/',
    package_dir={'': 'src'},
    packages=find_packages(where='./src'),
    license='GPL 2.0/LGPL 2.1',
    install_requires=(install_requires + extras_require),
    tests_require=tests_require,
    include_package_data=True,
)
