from django.urls import path
from .views import CategoryListAPI, ProductListAPI, ProductDetailAPI

urlpatterns = [
    path('categories/', CategoryListAPI.as_view(), name='api_categories'),
    path('', ProductListAPI.as_view(), name='api_products'),  # <-- note the empty string for base
    path('<slug:slug>/', ProductDetailAPI.as_view(), name='api_product_detail'),
]
