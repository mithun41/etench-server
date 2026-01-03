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

class ProductListAPI(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']  # search by name or description
    ordering_fields = ['price', 'created_at']  # allow ordering by price or date
    ordering = ['-created_at']  # default ordering

    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Filter by category ID or name
        category_id = self.request.query_params.get('category_id')
        category_name = self.request.query_params.get('category')

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        elif category_name:
            queryset = queryset.filter(category__name__iexact=category_name)
        
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
    search_fields = ['name']  # search by category name

    def get_queryset(self):
        # Annotate each category with product count
        return Category.objects.annotate(product_count=Count('product'))

# ----------------------
# URL Routing
# ----------------------
router = DefaultRouter()
router.register(r'products', ProductAdminViewSet, basename='products')  # admin CRUD

public_api_urls = [
    path('categories/', CategoryListAPI.as_view(), name='api_categories'),
    path('public/', ProductListAPI.as_view(), name='api_products_public'),
    path('public/<slug:slug>/', ProductDetailAPI.as_view(), name='api_product_detail_public'),
]

urlpatterns = router.urls + public_api_urls
