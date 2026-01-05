from rest_framework import viewsets, generics, permissions, filters
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

# ----------------------
# Admin CRUD API
# ----------------------
class CategoryAdminViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
class ProductAdminViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

# ----------------------
# Public Read-Only APIs
# ----------------------

# Custom pagination
class ProductPagination(PageNumberPagination):
    page_size = 10  # 10 products per page
    page_size_query_param = 'page_size'  # allow client to set page_size
    max_page_size = 50

from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from products.models import Product
from products.serializers import ProductSerializer
from products.pagination import ProductPagination


class ProductListAPI(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Product.objects.select_related("category").all()

        category_slug = self.request.query_params.get("category")
        subcategory_slug = self.request.query_params.get("subcategory")

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        if subcategory_slug:
            queryset = queryset.filter(subcategory__slug=subcategory_slug)

        return queryset


class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

class CategoryListAPI(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return Category.objects.annotate(
            product_count=Count('products')
        )


# ----------------------
# URL Routing
# ----------------------
router = DefaultRouter()
router.register(r'products', ProductAdminViewSet, basename='products')  # admin CRUD
router.register(r'admin/products', ProductAdminViewSet, basename='admin-products')
router.register(r'admin/categories', CategoryAdminViewSet, basename='admin-categories')
public_api_urls = [
    path('categories/', CategoryListAPI.as_view(), name='api_categories'),
    path('public/', ProductListAPI.as_view(), name='api_products_public'),
    path('public/<slug:slug>/', ProductDetailAPI.as_view(), name='api_product_detail_public'),
    
]

urlpatterns = router.urls + public_api_urls
