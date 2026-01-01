from django.contrib import admin
from .models import Order, CommissionTransaction

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'total_price', 'status', 'is_paid', 'affiliate', 'commission_added', 'created_at')
    list_filter = ('status', 'is_paid', 'created_at')
    search_fields = ('user__email', 'product__name', 'affiliate__user__email')
    readonly_fields = ('total_price', 'commission_added', 'created_at', 'updated_at')

    # allow inline status change in list view
    list_editable = ('status', 'is_paid')

@admin.register(CommissionTransaction)
class CommissionTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'affiliate', 'order', 'amount', 'created_at')
    search_fields = ('affiliate__user__email', 'order__id')
    readonly_fields = ('affiliate', 'order', 'amount', 'created_at')
