from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.models import Seller
from product.form import ProductForm
from product.models import OrderDetails, OrderItem, Product



def dashboard(request):
    seller = request.user.seller  

    orders = (
        OrderDetails.objects
        .filter(order_items__product__seller=seller)
        .prefetch_related('order_items')  
        .distinct().order_by('-created_at')[:5]
    )

    products_count = Product.objects.filter(seller=seller).count
    context = {
        'products_count':products_count,
        'orders':orders
    }

    return render(request, 'dashboard.html',context)


def is_seller(user):
    return user.groups.filter(name='Sellers').exists()
@login_required
@user_passes_test(is_seller,login_url='/account/login_as_seller')
def dashboardProducts(request):
    seller = request.user.seller
    order_items = OrderItem.objects.filter(product__seller=seller).select_related('order', 'product')

    orders = {}
    for item in order_items:
        order_id = item.order.order_id
        if order_id not in orders:
            orders[order_id] = {
                'order_id': order_id,
                'buyer': item.order.user,
                'created_at': item.order.created_at,
                'items': [],
            }
        orders[order_id]['items'].append(item)
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
        'user_products':user_products,
        'orders':orders
            }

    return render(request, "dashboard_products.html",context)

@login_required
@user_passes_test(is_seller,login_url='/account/login_as_seller')
def edit_product(request, product_id):
    product_by_id  = get_object_or_404(Product, product_id = product_id,seller__user = request.user)
    form = ProductForm(request.POST or None, request.FILES or None,instance=product_by_id)
    if request.method == 'POST':
        if form.is_valid():
            product_by_id.save()
            return redirect('dashboard_products')
        
    return render(request, 'edit_product.html',{'form':form,'product':product_by_id})

@login_required
@user_passes_test(is_seller, login_url='/account/login_as_seller')
def add_product(request):
      
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller
            product.save()
            return redirect('dashboard_products')
    else:
        form = ProductForm()

    return render(request, 'dashboard_add_product.html', {'form': form})


@login_required
@user_passes_test(is_seller, login_url='/account/login_as_seller')
def delete_product(request):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, product_id=product_id, seller__user=request.user)
    if product_id:
        product.delete()
        return redirect('dashboard_products')  
        
    return redirect('dashboard_products')

@login_required 
def dashboardOrders(request):
    seller = request.user.seller  

    orders = (
        OrderDetails.objects
        .filter(order_items__product__seller=seller)
        .prefetch_related('order_items')  
        .distinct().order_by('-created_at')
    )

    return render(request, 'dashboard_orders.html', {'orders': orders})