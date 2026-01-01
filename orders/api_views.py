from rest_framework import viewsets, permissions
from .models import Order, CommissionTransaction
from .serializers import OrderSerializer, CommissionTransactionSerializer

# Only logged-in users can see their own orders
class UserOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

# Admin-only access for all orders
class AdminOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.all()

class AdminCommissionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommissionTransactionSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = CommissionTransaction.objects.all()
