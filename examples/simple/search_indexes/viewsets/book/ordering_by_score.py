from .default import BookDocumentViewSet

__all__ = (
    'BookOrderingByScoreDocumentViewSet',
)


class BookOrderingByScoreDocumentViewSet(BookDocumentViewSet):
    """Same as BookDocumentViewSet, but sorted by _score."""

    search_fields = {
        'title': {'boost': 4},
        'summary': {'boost': 2},
        'description': None,
    }
    ordering = ('_score', 'id', 'title', 'price',)
