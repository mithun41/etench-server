from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer

class OrderCreateAPI(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
