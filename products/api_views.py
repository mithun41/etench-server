from rest_framework import viewsets, permissions, generics
from products.models import Product, Category
from products.serializers import ProductSerializer, CategorySerializer

# ----------------------
# Admin CRUD API
# ----------------------
class ProductAdminViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admin can CRUD

# ----------------------
# Public Read-Only API
# ----------------------
class CategoryListAPI(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
