
from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.models import Buyer
from  .models import CustomerAddress,CardData
from product.models import Cart,CartItem,OrderDetails,OrderItem
from django.contrib.auth.decorators import login_required
import uuid
from collections import defaultdict
from django.shortcuts import render, redirect



# Create your views here.

def checkout(request):
    mobile_number = request.POST.get('mobile_number', '')
    
    cardNumber = request.POST.get('cardNumber', '')
    
    if request.method == "POST":
            user = Buyer.objects.get(user=request.user)
            
            
            if cardNumber:
                cardData = CardData(
                    buyer = user,
                    card_number = cardNumber,
                    expire_date = request.POST.get('expire_date', ''),
                    cvv = request.POST.get('cvv', ''),
                    pincode = request.POST.get('pincode', ''),
                )
                print(cardNumber)
                cardData.save()
            elif mobile_number:
                address = CustomerAddress(
                buyer = user,
                country  = "India",
                full_name = request.POST.get('full_name', ''),
                mobile_number = mobile_number,
                pincode = request.POST.get('pincode', ''),
                address_line1 = request.POST.get('address_line1', ''),
                address_line2 = request.POST.get('address_line2', ''),
                state = request.POST.get('state', ''),
                city = request.POST.get('city', '')
                
            )
                print(mobile_number)
            
                address.save()
    customerAddress  = CustomerAddress.objects.filter(buyer__user= request.user)
    context = {
        'customerAddress': customerAddress,
        'cardNumber':cardNumber

    }
    return render(request, 'checkout.html', context)


def paymentSuccess(request):
    address_id = request.POST.get('address', '')
    user = Buyer.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart__user=user)
    
    customer_address = CustomerAddress.objects.filter(buyer=user, id=address_id).first()

    if customer_address:
        full_name = customer_address.full_name
        mobile_number = customer_address.mobile_number
        address = f"{customer_address.address_line1}, {customer_address.address_line2 or ''}, {customer_address.city}, {customer_address.state}, {customer_address.country}, {customer_address.pincode}"
    else:
        return redirect('checkout')

    seller_items = defaultdict(list)
    for item in cart_items:
        seller = item.product.seller
        seller_items[seller].append(item)

    for seller, items in seller_items.items():
        order_id = str(uuid.uuid4())
        order_details = OrderDetails(
            user=user,
            order_id=order_id,
        )
        order_details.save()

        for item in items:
            order_item = OrderItem(
                order=order_details,
                product=item.product,
                product_name=item.product.name,
                quantity=item.quantity,
                total_price=item.total_price,
                price=item.product.price,
                full_name=full_name,
                mobile_number=mobile_number,
                address=address,
            )
            order_item.save()

        print(f"Order for Seller: {seller}, Order ID: {order_id}")

    cart_items.delete()

    if request.method == "POST":
        if address_id:
            print(f"Selected address ID: {address_id}")
        else:
            print("No address selected")

        return render(request, 'payment_successful.html')
    
    return redirect('checkout')



@login_required 
def dashboardOrder(request):
    seller = request.user.seller  

    orders = (
        OrderDetails.objects
        .filter(order_items__product__seller=seller)
        .prefetch_related('order_items')  
        .distinct()
    )

    return render(request, 'product_dashboard_order.html', {'orders': orders})