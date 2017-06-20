from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections

from rest_framework.viewsets import ReadOnlyModelViewSet


__title__ = 'django_elasticsearch_dsl_drf.views'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2016-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('BaseDocumentViewSet',)


class BaseDocumentViewSet(ReadOnlyModelViewSet):
    """Base document viewset."""

    document = None  # Re-define

    def __init__(self, *args, **kwargs):
        assert self.document is not None

        self.client = connections.get_connection()
        self.index = self.document._doc_type.index
        self.mapping = self.document._doc_type.mapping.properties.name
        self.search = Search(using=self.client, index=self.index)
        super(BaseDocumentViewSet, self).__init__(*args, **kwargs)

    def get_queryset(self):
        """Get queryset."""
        return self.search.query()
