from django.conf import settings
from rest_framework import serializers
from .models import Order, CommissionTransaction, WithdrawRequest
from products.models import Product
from affiliates.models import Affiliate
from django.contrib.auth import get_user_model
# --------------------------
User = get_user_model()  # actual model class

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'role']  # adjust to your user model

# --------------------------
# Product Info Serializer
# --------------------------
class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'slug']

# --------------------------
# Affiliate Info Serializer
# --------------------------
class AffiliateInfoSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    class Meta:
        model = Affiliate
        fields = ['id', 'referral_code', 'user']

# --------------------------
# Order Serializer
# --------------------------
class OrderSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    product = ProductInfoSerializer(read_only=True)
    affiliate = AffiliateInfoSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('total_price', 'commission_added', 'created_at', 'updated_at')

# --------------------------
# Commission Serializer
# --------------------------
class CommissionTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionTransaction
        fields = '__all__'
        read_only_fields = ('affiliate', 'order', 'amount', 'created_at')

class AffiliateCommissionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='order.product.name', read_only=True)
    order_id = serializers.IntegerField(source='order.id', read_only=True)

    class Meta:
        model = CommissionTransaction
        fields = [
            'id',
            'order_id',
            'product_name',
            'amount',
            'status',
            'created_at',
        ]

# --------------------------
# Withdraw Request Serializer
# --------------------------
class WithdrawRequestSerializer(serializers.ModelSerializer):
    affiliate = AffiliateInfoSerializer(read_only=True)
    class Meta:
        model = WithdrawRequest
        fields = '__all__'
        read_only_fields = ('status', 'created_at', 'processed_at')
