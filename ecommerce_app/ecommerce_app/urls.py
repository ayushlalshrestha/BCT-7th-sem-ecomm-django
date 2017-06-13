from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from carts.views import ItemCountView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^products/', include('products.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^carts/', include('carts.urls')),
    url(r'^cart/count/$', ItemCountView.as_view(), name='item_count'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
