from django.urls import path
from .views import OrderCreateAPI

urlpatterns = [
    path('create/', OrderCreateAPI.as_view(), name='api_order_create'),
]
