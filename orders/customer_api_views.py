from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from decimal import Decimal

from .models import Order, WithdrawRequest
from .serializers import OrderSerializer, WithdrawRequestSerializer
from products.models import Product
from affiliates.models import Affiliate


class CustomerOrderListCreateAPI(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

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


class WithdrawRequestAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        affiliate = getattr(request.user, 'affiliate', None)
        if not affiliate:
            return Response({"detail": "You are not an affiliate"}, status=403)

        amount = request.data.get('amount')
        if not amount:
            return Response({"detail": "Amount is required"}, status=400)

        # Convert to Decimal for accuracy
        amount = Decimal(amount)

        # Validate amount <= available commission
        available = affiliate.total_commission
        if amount > available:
            return Response({"detail": "Requested amount exceeds available commission"}, status=400)

        withdraw = WithdrawRequest.objects.create(
            affiliate=affiliate,
            amount=amount
        )

        serializer = WithdrawRequestSerializer(withdraw)
        return Response(serializer.data, status=201)
