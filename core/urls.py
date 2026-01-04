from django.contrib import admin
from django.urls import path, include

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
