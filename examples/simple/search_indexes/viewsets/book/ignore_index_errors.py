from .default import BookDocumentViewSet

__all__ = (
    'BookIgnoreIndexErrorsDocumentViewSet',
)


class BookIgnoreIndexErrorsDocumentViewSet(BookDocumentViewSet):
    """Book document view set based on compound search backend."""

    ignore = [404]
