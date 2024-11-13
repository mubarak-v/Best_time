from django.urls import  path
from . import views
from checkout.views import dashboardOrder

urlpatterns = [
  
    path('', views.products, name = "products"),
    path('<int:pk>/', views.product_details, name = "products_details"),
    path('cart/', views.cart_view, name="cart_view"),
    path('cart/add/<int:product_id>/<str:action>/', views.add_cart, name='add_cart'),
    path('cart/remove/<int:product_id>', views.delete_cart_product , name = 'delete_cart_product'),
    path('list', views.productList, name = 'productList'),
    
    



]