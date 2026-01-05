from django.contrib import admin
from django.urls import path, include
from django.conf import settings # এটি ইমপোর্ট করুন
from django.conf.urls.static import static # এটি ইমপোর্ট করুন

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Auth
    path('api/auth/', include('users.jwt_urls')),

    # Customer APIs
    path('api/', include('orders.customer_api_urls')),  # ✅ only once

    # Admin order management
    path('api/admin/orders/', include('orders.api_urls')),

    # Products APIs
    path('api/products/', include('products.api_views')),

    # Admin user management
    path('api/admin/', include('users.api_urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)