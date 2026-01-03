from django.urls import path
from .api_views import AdminDashboardSummaryAPI

urlpatterns = [
    path('dashboard-summary/', AdminDashboardSummaryAPI.as_view(), name='admin_dashboard_summary'),
]
