import os

from setuptools import find_packages, setup

try:
    readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
except:
    readme = ''

version = '0.1.2'

install_requires = [
    'six>=1.9',
    'django-nine>=0.1.10',
    'django-elasticsearch-dsl',
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
    'tox'
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
