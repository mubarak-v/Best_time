from django.urls import  path
from . import views

urlpatterns = [
  
            path('/', views.checkout, name = "checkout"),
            path('payment_success/', views.paymentSuccess, name = "payment_success"),

            


]