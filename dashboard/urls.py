from django.urls import  path
from . import views


urlpatterns = [

    path('',views.dashboard, name = "dashboard"),
    path('orders/',views.dashboardOrders, name = "dashboard_orders")

]