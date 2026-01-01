from rest_framework import serializers
from .models import Order, CommissionTransaction

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('total_price', 'commission_added', 'created_at', 'updated_at')

class CommissionTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionTransaction
        fields = '__all__'
        read_only_fields = ('affiliate', 'order', 'amount', 'created_at')
