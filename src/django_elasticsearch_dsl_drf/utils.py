__title__ = 'django_elasticsearch_dsl_drf.utils'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2016-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'EmptySearch',
)


class EmptySearch(object):
    """Empty Search."""

    def __init__(self, **kwargs):
        pass

    def __len__(self):
        return 0

    def __iter__(self):
        return iter([])
