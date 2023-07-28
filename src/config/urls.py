from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('secretadminpanel/', admin.site.urls),
    path('', include('products.urls')),
    path('', include('payments.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # import debug_toolbar
    #
    # urlpatterns += [
    #     path('__debug__/', include(debug_toolbar.urls)),
    # ]
    # urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
