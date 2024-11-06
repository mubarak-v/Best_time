from django.urls import  path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import messages

class CustomLogoutView(auth_views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.SUCCESS, 'You have successfully logged out.')
        return super().dispatch(request, *args, **kwargs)

urlpatterns = [
  
    path('login_as_seller/', views.seller, name = "login_as_seller"),
    path('login_as_buyer/', views.buyer, name = "login_as_buyer"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),


 

    
]
