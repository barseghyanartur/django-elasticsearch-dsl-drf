from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedFilterSearchFilterBackend,
)

from .base import BaseBookDocumentViewSet


__all__ = (
    'FacetedFilteredBookDocumentViewSet',
)


class FacetedFilteredBookDocumentViewSet(BaseBookDocumentViewSet):
    """The BookDocument view with faceted filtering."""

    filter_backends = [
        FacetedFilterSearchFilterBackend,
        DefaultOrderingFilterBackend,
    ]

    filter_fields = {
        'title': 'title.raw',
        'state': 'state.raw',
    }

    faceted_search_fields = {
        'state': 'state.raw',
    }
