from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    PostFilterFilteringFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import (
    MoreLikeThisMixin,
)

from .base import BaseBookDocumentViewSet

__all__ = (
    'BookMoreLikeThisDocumentViewSet',
    'BookMoreLikeThisNoOptionsDocumentViewSet',
)


class BookMoreLikeThisDocumentViewSet(BaseBookDocumentViewSet,
                                      MoreLikeThisMixin):
    """Same as BookDocumentViewSet, with more-like-this and no facets."""

    filter_backends = [
        FilteringFilterBackend,
        PostFilterFilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        # DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]

    # More-like-this options
    more_like_this_options = {
        'fields': (
            'title.mlt',
            'summary.mlt',
            'description.mlt',
            # 'title.raw',
            # 'summary.raw',
            # 'description.raw',
            # 'authors',
            # 'tags.raw',
        ),
        # 'min_term_freq': 1,
        # 'max_query_terms': 25,
        # "unlike": ['chapter', 'CHAPTER'],
    }


class BookMoreLikeThisNoOptionsDocumentViewSet(BaseBookDocumentViewSet,
                                               MoreLikeThisMixin):
    """Same as BookDocumentViewSet, with more-like-this and no facets."""

    filter_backends = [
        FilteringFilterBackend,
        PostFilterFilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        # DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
