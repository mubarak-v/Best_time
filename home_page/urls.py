from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  
    path('', views.home, name = "home"),
    path('link/', views.link, name = "link")
    
]


