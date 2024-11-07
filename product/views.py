from decimal import Decimal
from django.shortcuts import redirect, render
from .form import ProductForm,ReviewForm
from .models import Cart, Product,Review,CartItem,Cart
from accounts.models import Buyer
from django.shortcuts import get_object_or_404
from accounts.models import Buyer, Seller
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.
# python django inheritance

def products(request):

    context ={
        
        'products': Product.objects.all()  
    }
    return render(request,"index.html" , context)

def product_details(request,pk):
    reviewForm = ReviewForm(request.POST)
    if request.method == 'POST':
        if reviewForm.is_valid:
            review = reviewForm.save(commit=False)
            review.product = Product.objects.get(product_id = pk)
            review.reviewer_name = request.user.username
            review.save()
    product_details = Product.objects.filter(product_id = pk)
    Reviews = Review.objects.filter(product__product_id = pk)
    context ={
        'reviewForm':reviewForm,
        'product_details': product_details,
        'Reviews':Reviews

    }
    return render(request, "product_details.html", context)

def is_seller(user):
    return user.groups.filter(name='Sellers').exists()

@login_required
@user_passes_test(is_seller,login_url='/account/login_as_seller')
def product_dashboard(request):
    try:
        seller_instance = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        return redirect('/account/login_as_seller') 
    user_products = Product.objects.filter(seller=seller_instance)

    form = ProductForm(request.POST,request.FILES)

    if request.method == 'POST':
        if form.is_valid():
            products = form.save(commit=False)
            products.seller = request.user.seller
            products.save()

            return redirect('dashboard')
    context = {
        'form': form,
        'user_products':user_products
            }

    return render(request, "product_dashboard.html",context)
    
@login_required
@user_passes_test(is_seller,login_url='/account/login_as_seller')
def edit_product(request, product_id):
    product_by_id  = get_object_or_404(Product, product_id = product_id,seller__user = request.user)
    form = ProductForm(request.POST or None, request.FILES or None,instance=product_by_id)
    if request.method == 'POST':
        if form.is_valid():
            product_by_id.save()
            return redirect('dashboard')
        
    return render(request, 'edit_product.html',{'form':form,'product':product_by_id})


@login_required
@user_passes_test(is_seller, login_url='/account/login_as_seller')
def add_product(request):
    print("View is called")  # Debugging line
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller
            product.save()
            return redirect('dashboard')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


@login_required
@user_passes_test(is_seller, login_url='/account/login_as_seller')
def delete_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id, seller__user=request.user)
    
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard')  

    return redirect('dashboard')
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
    # views.py
    print( totalPrice)


    context = {
        'items': cart_items,
        'cart_items_length':cart_items_length, 
        'total_price': totalPrice,
        'total_with_shipping': totalPrice + Decimal('40.00')
    }

    return render(request, 'cart.html', context)




def add_cart(request, product_id, action):
    if not request.user.is_authenticated:
        # Redirect to the login page if not authenticated
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