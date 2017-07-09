from django.conf.urls import url, include
from rest_framework_extensions.routers import ExtendedDefaultRouter

from .viewsets import BookDocumentViewSet, PublisherDocumentViewSet

__all__ = ('urlpatterns',)

router = ExtendedDefaultRouter()
books = router.register(r'books',
                        BookDocumentViewSet,
                        base_name='bookdocument')
publishers = router.register(r'publishers',
                             PublisherDocumentViewSet,
                             base_name='publisherdocument')

urlpatterns = [
    url(r'^', include(router.urls)),
]
