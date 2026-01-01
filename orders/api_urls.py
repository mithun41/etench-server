from rest_framework.routers import DefaultRouter
from .api_views import UserOrderViewSet, AdminOrderViewSet, AdminCommissionViewSet

router = DefaultRouter()
router.register('my-orders', UserOrderViewSet, basename='user-orders')
router.register('orders', AdminOrderViewSet, basename='admin-orders')
router.register('commissions', AdminCommissionViewSet, basename='admin-commissions')

urlpatterns = router.urls
