from decimal import Decimal
from tempfile import template
from django.shortcuts import redirect, render
from .form import ProductForm,ReviewForm
from .models import Cart, Product,Review,CartItem,Cart
from accounts.models import Buyer
from django.shortcuts import get_object_or_404
from accounts.models import Buyer, Seller
from django.contrib.auth.decorators import login_required,user_passes_test
from product.models import OrderItem

# Create your views here.
# python django inheritance

def products(request):
    products = Product.objects.all()
    # Filter products where brand is either "Fossil" or "Amazfit"
    brand1 = request.GET.get('brand1')
    brand2 =  request.GET.get('brand2')
    print(brand1, brand2)
    if brand1 and brand2:
        filtered_products = Product.objects.filter(brand__in=[brand1,brand2])
    else:
        filtered_products = Product.objects.order_by('-price')[:5]

    

    context ={
        
        'products': filtered_products 
    }
    return render(request,"index.html" , context)

def product_details(request,pk):
    reviewForm = ReviewForm(request.POST)
    
    if request.method == 'POST':
        if reviewForm.is_valid and request.user.is_authenticated:
            review = reviewForm.save(commit=False)
            review.product = Product.objects.get(product_id = pk)
            review.reviewer_name = request.user.username
            review.save()
        else:
            return redirect('login')
    product_details = Product.objects.filter(product_id = pk)
    Reviews = Review.objects.filter(product__product_id = pk)
    context ={
        'reviewForm':reviewForm,
        'product_details': product_details,
        'Reviews':Reviews

    }
    return render(request, "product_details.html", context)


def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('/account/login')
    totalPrice = Decimal('0.00')
    user = get_object_or_404(Buyer, user=request.user)
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = cart.cart_items.all()
    
    for total in cart_items:
        price = total.total_price
        totalPrice += price
        
    cart_items_length = len(cart_items)
    


    context = {
        'items': cart_items,
        'cart_items_length':cart_items_length, 
        'total_price': totalPrice,
        'total_with_shipping': totalPrice + Decimal('40.00')
    }

    return render(request, 'cart.html', context)



def add_cart(request, product_id, action):
    if not request.user.is_authenticated:
        return redirect('/account/login')
    product = get_object_or_404(Product, product_id=product_id)
    user = get_object_or_404(Buyer, user=request.user)
    
    cart, created = Cart.objects.get_or_create(user=user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if action == "Increase":
        cart_item.quantity += 1
    elif action == "Decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()  
            return redirect('cart_view')

    cart_item.save()  

    return redirect('cart_view')  

def delete_cart_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    user = get_object_or_404(Buyer, user=request.user)
    
    cart, created = Cart.objects.get_or_create(user=user)

    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()  

    return redirect('cart_view')

def productList(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})