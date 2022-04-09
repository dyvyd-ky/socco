
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('vendors/', include('apps.vendor.urls')),
    path('cart/', include('apps.cart.urls')),
    path('users/', include('apps.users.urls')),
    path('', include('apps.core.urls')),
    path('', include('apps.product.urls')),
    path('accounts/', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
