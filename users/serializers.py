# users/serializers.py or dashboard/serializers.py
from rest_framework import serializers

class DashboardSummarySerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    total_products = serializers.IntegerField()
    total_orders = serializers.IntegerField()
    total_commissions = serializers.DecimalField(max_digits=12, decimal_places=2)
