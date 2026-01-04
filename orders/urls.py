from django.urls import path
from .views import OrderCreateAPI, MyCommissionListAPI

urlpatterns = [
    path('create/', OrderCreateAPI.as_view(), name='api_order_create'),
    path('affiliate/commissions/', MyCommissionListAPI.as_view(), name='affiliate_commissions'),
]
