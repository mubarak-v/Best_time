from django.urls import  path
from . import views
from checkout.views import dashboardOrder

urlpatterns = [
  
    path('', views.products, name = "products"),
    path('<int:pk>/', views.product_details, name = "products_details"),
    path('dashboard/', views.product_dashboard, name = "dashboard"),
    path('dashboard/edit/<int:product_id>/', views.edit_product, name="edit_product"),
    path('dashboard/add/', views.add_product, name="add_product"),
    path('dashboard/delete/<int:product_id>/', views.delete_product, name="delete_product"),
    path('cart/', views.cart_view, name="cart_view"),
    path('cart/add/<int:product_id>/<str:action>/', views.add_cart, name='add_cart'),
    path('cart/remove/<int:product_id>', views.delete_cart_product , name = 'delete_cart_product'),
    path('list', views.productList, name = 'productList'),
    
    



]