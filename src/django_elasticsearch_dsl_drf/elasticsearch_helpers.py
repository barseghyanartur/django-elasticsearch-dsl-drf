from anysearch.search import AnySearch
from django.conf import settings

__title__ = 'django_elasticsearch_dsl_drf.elasticsearch_helpers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2022 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    "get_all_indices",
    "delete_all_indices",
)


def get_all_indices(with_protected=False):
    """Get all indices.
    Args:
        with_protected (bool):
    Returns:
        list: List of indices.
    """
    es = AnySearch(**settings.ELASTICSEARCH_DSL["default"])
    _indices = es.indices.get_alias("*").items()
    if with_protected:
        return [_i for _i, _o in _indices]
    else:
        return [_i for _i, _o in _indices if not _i.startswith(".")]


def delete_all_indices(with_protected=False):
    """Delete all indices.
    Args:
        with_protected (bool):
    Returns:
        tuple: Tuple of two lists with removed and errored indices.
    """
    es = AnySearch(**settings.ELASTICSEARCH_DSL["default"])
    _indices = get_all_indices(with_protected=with_protected)
    _ok = []
    _fail = []
    for _i in _indices:
        try:
            _res = es.indices.delete(_i)
        except Exception as err:
            _fail.append(_i)
        if _res and isinstance(_res, dict) and _res.get("acknowledged", False):
            _ok.append(_i)
    return _ok, _fail
