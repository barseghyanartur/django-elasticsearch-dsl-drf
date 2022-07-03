from django_elasticsearch_dsl_drf.utils import EmptySearch

from .default import BookDocumentViewSet

__all__ = (
    'BookNoRecordsDocumentViewSet',
)


class BookNoRecordsDocumentViewSet(BookDocumentViewSet):
    """Book document view set based on compound search backend."""

    def get_queryset(self):
        queryset = EmptySearch()
        queryset.model = self.document.Django.model
        return queryset
