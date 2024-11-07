from django.shortcuts import render
from product.models import Product

# Create your views here.
# home_page/views.py

from django.shortcuts import render
def home(request):
    # products = Product.objects.all()
    # Filter products where brand is either "Fossil" or "Amazfit"
    # filtered_products = Product.objects.filter(brand__in=["fossil", "amazfit"])
    products = Product.objects.all()[:10]

    context = {
        'products': products,
        
    }
    
    return render(request, 'home_page.html', context)
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')


