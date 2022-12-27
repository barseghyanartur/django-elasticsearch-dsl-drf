import os

from setuptools import find_packages, setup

version = '0.23'

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
        ':doc:`Post-filter filter backend <advanced_usage_examples>`',
        '`Post-filter filter backend <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'advanced_usage_examples.html#post-filter'
        '>`_'.format(version)
    ),
    (
        ':doc:`Nested filtering filter backend <nested_fields_usage_examples>`',
        '`Nested filtering filter backend <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'nested_fields_usage_examples.html#nested-filtering'
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
        ':doc:`Functional suggester filter backend <advanced_usage_examples>`',
        '`Functional suggester filter backend <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'advanced_usage_examples.html#functional-suggestions'
        '>`_'.format(version)
    ),
    (
        ':doc:`Ids filter backend <advanced_usage_examples>`',
        '`Ids filter backend <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'advanced_usage_examples.html#ids-filter'
        '>`_'.format(version)
    ),
    (
        ':doc:`Multi match search filter backend <search_backends>`',
        '`Multi match search filter backend <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'search_backends.html#multi-match-search-filter-backend'
        '>`_'.format(version)
    ),
    (
        ':doc:`Simple search query search filter backend <search_backends>`',
        '`Simple search query filter backend <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'search_backends.html#simple-query-string-filter-backend'
        '>`_'.format(version)
    ),
    (
        ':doc:`More-like-this support (detail action) <more_like_this>`',
        '`More-like-this support (detail action) <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'more_like_this.html'
        '>`_'.format(version)
    ),
    (
        ':doc:`Global aggregations support <global_aggregations>`',
        '`Global aggregations support <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'global_aggregations.html'
        '>`_'.format(version)
    ),
    (
        ':doc:`Source filter backend <source_backend>`',
        '`Source filter backend <'
        'http://django-elasticsearch-dsl-drf.readthedocs.io/en/{}/'
        'source_backend.html'
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
    'django-nine>=0.2',
    'djangorestframework',
    'anysearch>=0.1.7',
]

extras_require = []

tests_require = [
    'factory_boy',
    'Faker',
    'pytest',
    'pytest-django',
    'pytest-cov',
    'tox',
    'mock',
]

setup(
    name='django-elasticsearch-dsl-drf',
    version=version,
    description="Integrate Elasticsearch DSL with Django REST framework.",
    long_description=readme,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Environment :: Web Environment",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or "
        "later (LGPLv2+)",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/barseghyanartur/"
                       "django-elasticsearch-dsl-drf/issues",
        "Documentation": "https://django-elasticsearch-dsl-drf.readthedocs.io/",
        "Source Code": "https://github.com/barseghyanartur/"
                       "django-elasticsearch-dsl-drf",
        "Changelog": "https://django-elasticsearch-dsl-drf.readthedocs.io/"
                     "en/latest/changelog.html",
    },
    keywords="django, elasticsearch, elasticsearch-dsl, "
             "django-elasticsearch-dsl, opensearch, opensearch-dsl, "
             "django-opensearch-dsl, django-rest-framework",
    author='Artur Barseghyan',
    author_email='artur.barseghyan@gmail.com',
    url='https://github.com/barseghyanartur/django-elasticsearch-dsl-drf/',
    package_dir={'': 'src'},
    packages=find_packages(where='./src'),
    license='GPL-2.0-only OR LGPL-2.1-or-later',
    python_requires=">=3.6",
    install_requires=(install_requires + extras_require),
    extras_require={
        "elasticsearch": [
            "elasticsearch",
            "elasticsearch-dsl",
            "django-elasticsearch-dsl>=6.4.1",
        ],
        "opensearch": [
            "opensearch",
            "opensearch-dsl",
            "django-opensearch-dsl",
        ],
    },
    tests_require=tests_require,
    include_package_data=True,
)
