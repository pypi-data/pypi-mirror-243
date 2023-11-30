from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import *
from django.urls.conf import include 
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('', include('siteapp.urls', namespace='site')), 
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('nexus/', include('nexus.urls', namespace='nexus')),
    path('linkzone/', include('linkzone.urls', namespace='linkzone')), 
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
