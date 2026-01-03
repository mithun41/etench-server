from rest_framework import viewsets, permissions
from .models import Order, CommissionTransaction
from .serializers import OrderSerializer, CommissionTransactionSerializer

# Logged-in user can see only their orders
class UserOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

# Admin-only for all orders
class AdminOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = Order.objects.all()

# Admin-only commissions (read-only)
class AdminCommissionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommissionTransactionSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = CommissionTransaction.objects.all()
