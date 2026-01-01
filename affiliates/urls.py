from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.affiliate_dashboard, name='affiliate_dashboard'),
]
