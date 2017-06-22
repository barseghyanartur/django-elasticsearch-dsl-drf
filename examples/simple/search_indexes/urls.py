from django.conf.urls import url, include
from rest_framework_extensions.routers import ExtendedDefaultRouter

from .views import BookDocumentView, PublisherDocumentView

__all__ = ('urlpatterns',)

router = ExtendedDefaultRouter()
books = router.register(r'books',
                        BookDocumentView,
                        base_name='bookdocument')
publishers = router.register(r'publishers',
                             PublisherDocumentView,
                             base_name='publisherdocument')

urlpatterns = [
    url(r'^', include(router.urls)),
]
