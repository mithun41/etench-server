from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import Order
from .serializers import OrderSerializer
from products.models import Product
from affiliates.models import Affiliate


class CustomerOrderListCreateAPI(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]  # JWT required

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        product_id = self.request.data.get("product_id")
        quantity = int(self.request.data.get("quantity", 1))
        ref_code = self.request.query_params.get("ref")

        product = get_object_or_404(Product, id=product_id)

        # Validate affiliate
        affiliate = None
        if ref_code:
            affiliate = Affiliate.objects.filter(referral_code=ref_code, is_active=True).first()

        # Save order with affiliate if valid
        serializer.save(
            user=self.request.user,
            product=product,
            quantity=quantity,
            affiliate=affiliate,
            status='pending',
            is_paid=False
        )
