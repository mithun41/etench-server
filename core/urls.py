from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth (JWT)
    path('api/auth/', include('users.jwt_urls')),

    # Products APIs (admin + public)
    path('api/products/', include('products.api_views')),

    # Customer order APIs
    path("api/customer/", include("orders.customer_api_urls")),

    # Admin order management
    path('api/admin/orders/', include('orders.api_urls')),
    path('api/admin/', include('users.api_urls')),
]
