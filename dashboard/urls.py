from django.urls import  path
from . import views


urlpatterns = [

    path('',views.dashboard, name = "dashboard"),
    path('orders/',views.dashboardOrders, name = "dashboard_orders"),
    path('products/',views.dashboardProducts, name = "dashboard_products"),
    path('products/edit/<int:product_id>/',views.edit_product, name = "dashboard_products_edit"),
    path('products/add/', views.add_product, name = "dashboard_products_add"),
    path('products/delete/', views.delete_product, name="delete_product"),


]