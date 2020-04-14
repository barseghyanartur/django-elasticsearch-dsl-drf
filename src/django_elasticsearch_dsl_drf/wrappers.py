import json
from six import python_2_unicode_compatible

__title__ = 'django_elasticsearch_dsl_drf.wrappers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2020 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'dict_to_obj',
    'obj_to_dict',
    'Wrapper',
)


@python_2_unicode_compatible
class Wrapper(object):
    """Wrapper.

    Example:
    >>> from django_elasticsearch_dsl_drf.wrappers import dict_to_obj
    >>>
    >>> mapping = {
    >>>     'country': {
    >>>         'name': 'Netherlands',
    >>>         'province': {
    >>>             'name': 'North Holland',
    >>>             'city': {
    >>>                 'name': 'Amsterdam',
    >>>             }
    >>>         }
    >>>     }
    >>> }
    >>>
    >>> wrapper = dict_to_obj(mapping)
    >>> wrapper.country.name
    >>> "Netherlands"
    >>> wrapper.country.province.name
    >>> "North Holland"
    >>> wrapper.country.province.city.name
    >>> "Amsterdam"
    >>> wrapper.as_dict
    >>> {
    >>>     'country': {
    >>>         'name': 'Netherlands',
    >>>         'province': {
    >>>             'name': 'North Holland',
    >>>             'city': {
    >>>                 'name': 'Amsterdam',
    >>>             }
    >>>         }
    >>>     }
    >>> }
    >>> str(wrapper)
    >>> "Netherlands"
    """

    def __str__(self):
        for key, item in self.__dict__.items():
            if isinstance(item, Wrapper):
                return item.__str__()
            else:
                return item

    @property
    def as_dict(self):
        """As dict.

        :return:
        :rtype: dict
        """
        return obj_to_dict(self)

    @property
    def as_json(self):
        """As JSON.

        :return:
        :rtype: str
        """
        return json.dumps(self.as_dict)


def dict_to_obj(mapping):
    """dict to obj mapping.

    :param mapping:
    :type mapping: dict
    :return:
    :rtype: :obj:`Wrapper`
    """
    wrapper = Wrapper()

    for key, item in mapping.items():
        if isinstance(item, dict):
            setattr(wrapper, key, dict_to_obj(item))
        else:
            setattr(wrapper, key, item)
    return wrapper


def obj_to_dict(obj):
    """Wrapper to dict.

    :param obj:
    :type obj: `obj`:Wrapper:
    :return:
    :rtype: dict
    """
    mapping = {}

    for key, item in obj.__dict__.items():
        if isinstance(item, Wrapper):
            mapping.update({key: obj_to_dict(item)})
        else:
            mapping.update({key: item})

    return mapping
