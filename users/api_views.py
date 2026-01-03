# dashboard/api_views.py (or any relevant app)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from products.models import Product
from orders.models import Order, CommissionTransaction
from django.db import models


User = get_user_model()

class AdminDashboardSummaryAPI(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        total_users = User.objects.count()
        total_products = Product.objects.count()
        total_orders = Order.objects.count()
        total_commissions = CommissionTransaction.objects.aggregate(
            total=models.Sum('amount')
        )['total'] or 0

        data = {
            "total_users": total_users,
            "total_products": total_products,
            "total_orders": total_orders,
            "total_commissions": total_commissions
        }

        return Response(data)
