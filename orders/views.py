from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum

from .models import CommissionTransaction
from .serializers import AffiliateCommissionSerializer

class OrderCreateAPI(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class MyCommissionListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        affiliate = getattr(request.user, 'affiliate', None)

        if not affiliate:
            return Response(
                {"detail": "You are not an affiliate"},
                status=403
            )

        qs = CommissionTransaction.objects.filter(
            affiliate=affiliate
        ).order_by('-created_at')

        serializer = AffiliateCommissionSerializer(qs, many=True)

        summary = {
            'pending': qs.filter(status='pending').aggregate(
                total=Sum('amount')
            )['total'] or 0,
            'approved': qs.filter(status='approved').aggregate(
                total=Sum('amount')
            )['total'] or 0,
            'paid': qs.filter(status='paid').aggregate(
                total=Sum('amount')
            )['total'] or 0,
        }

        return Response({
            'summary': summary,
            'commissions': serializer.data
        })
