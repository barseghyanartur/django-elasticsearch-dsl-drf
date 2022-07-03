"""
Integrate Elasticsearch DSL with Django REST framework.
"""

__title__ = 'django-elasticsearch-dsl-drf'
__version__ = '0.22.5'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2022 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'


from django_nine import versions

if versions.DJANGO_LTE_3_1:
    __all__ = ('default_app_config',)
    default_app_config = 'django_elasticsearch_dsl_drf.apps.Config'
