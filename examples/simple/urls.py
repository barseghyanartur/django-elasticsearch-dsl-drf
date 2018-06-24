from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import TemplateView

from nine import versions

from books import urls as books_urls
from search_indexes import urls as search_index_urls

__all__ = ('urlpatterns',)

admin.autodiscover()

urlpatterns = []
urlpatterns_args = []

if versions.DJANGO_GTE_2_0:
    urlpatterns_args += [
        url(r'^admin/', admin.site.urls),
    ]
else:
    urlpatterns_args += [
        url(r'^admin/', include(admin.site.urls)),
    ]

urlpatterns_args += [
    # Books URLs
    url(r'^books/', include(books_urls)),

    # Search URLs
    url(r'^search/', include(search_index_urls)),

    # Home page
    url(r'^$', TemplateView.as_view(template_name='home.html')),
]

urlpatterns += urlpatterns_args[:]

# Serving media and static in debug/developer mode.
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    if settings.DEBUG_TOOLBAR is True:
        import debug_toolbar

        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
