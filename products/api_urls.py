from rest_framework.routers import DefaultRouter
from products.api_views import ProductAdminViewSet, CategoryListAPI, ProductListAPI, ProductDetailAPI
from django.urls import path

# Admin CRUD API
router = DefaultRouter()
router.register(r'products', ProductAdminViewSet, basename='products')

# Public Read-Only API
public_api_urls = [
    path('categories/', CategoryListAPI.as_view(), name='api_categories'),
    path('public/', ProductListAPI.as_view(), name='api_products_public'),
    path('public/<slug:slug>/', ProductDetailAPI.as_view(), name='api_product_detail_public'),
]

# Combine URLs
urlpatterns = router.urls + public_api_urls
