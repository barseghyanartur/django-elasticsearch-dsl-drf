"""
Transitional compatibility module. Contains various field wrappers and
helpers for painless (testing of) Elastic 2.x to Elastic 5.x transition. This
module is not supposed to solve all transition issues for you. Better move to
Elastic 5.x as soon as possible.
"""

from django_elasticsearch_dsl import fields

# For compatibility reasons
from .versions import get_elasticsearch_version

try:
    import coreapi
except ImportError:
    coreapi = None

try:
    import coreschema
except ImportError:
    coreschema = None

# try:
#     from rest_framework.pagination import _get_count
# except ImportError:
#     _get_count = None

__title__ = 'django_elasticsearch_dsl_drf.compat'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'coreapi',
    'coreschema',
    # 'get_count',
    'KeywordField',
    'StringField',
)


# def get_count(self, queryset):
#     """Get count.
#
#     :param self:
#     :param queryset:
#     :return:
#     """
#     if _get_count is None:
#         return self.get_count(queryset)
#     else:
#         return _get_count(queryset)


KeywordField = fields.KeywordField


def string_field(**kwargs):
    """String field.

    :param kwargs:
    :return:
    """
    kwargs.setdefault('fielddata', True)
    return fields.TextField(**kwargs)


StringField = string_field


def nested_sort_entry(path, split_path=True):
    """String field.
    :param path: Full path to nested container, separated by period
    :param split_path: Indicates if each section of a path should have a nested query created
    :type path: str
    :type split_path: bool
    :return: Dictionary of full nested path
    :rtype: dict
    """
    version = get_elasticsearch_version()
    if version[0] < 6 or (version[0] == 6 and version[1] < 1):
        return {'nested_path': path}
    nested_path = {}
    path_list = path.split('.') if split_path else [path]
    for _ in reversed(path_list):
        if nested_path:
            nested_path = {'path': '.'.join(path_list), 'nested': nested_path}
        else:
            nested_path = {'path': '.'.join(path_list)}
        path_list.pop()
    return {'nested': nested_path}
