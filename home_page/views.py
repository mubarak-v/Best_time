from django.shortcuts import render
from product.models import Product

# Create your views here.
# home_page/views.py

from django.shortcuts import render
def home(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    # print(Products)
    return render(request, 'home_page.html', context)
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')


