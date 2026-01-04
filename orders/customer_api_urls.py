from django.urls import path
from .customer_api_views import CustomerOrderListCreateAPI, WithdrawRequestAPI

urlpatterns = [
    path("orders/", CustomerOrderListCreateAPI.as_view(), name="customer_orders"),
    path("orders/withdraw-request/", WithdrawRequestAPI.as_view(), name="affiliate_withdraw_request"),
]
