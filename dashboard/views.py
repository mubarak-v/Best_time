from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from product.models import OrderDetails

def dashboard(request):
    return render(request, 'dashboard.html')
@login_required 
def dashboardOrders(request):
    seller = request.user.seller  

    orders = (
        OrderDetails.objects
        .filter(order_items__product__seller=seller)
        .prefetch_related('order_items')  
        .distinct().order_by('-created_at')
    )

    return render(request, 'dashboard_orders.html', {'orders': orders})