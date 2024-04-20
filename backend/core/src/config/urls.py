from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('secretadminpanel/', admin.site.urls),
    path('', include('products.urls')),
    path('', include(('payments.presentators.api.v1.urls', 'payments'), namespace='payments')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
