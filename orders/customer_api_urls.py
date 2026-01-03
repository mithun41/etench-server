from django.urls import path
from .customer_api_views import CustomerOrderListCreateAPI

urlpatterns = [
    path("orders/", CustomerOrderListCreateAPI.as_view(), name="customer_orders"),
]
