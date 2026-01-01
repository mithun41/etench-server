from django.shortcuts import render
from .models import Affiliate

def affiliate_dashboard(request):
    affiliate = request.user.affiliate  # assuming user is logged in
    orders = affiliate.orders.all()
    context = {
        'affiliate': affiliate,
        'orders': orders
    }
    return render(request, 'affiliates/dashboard.html', context)
