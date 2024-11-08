from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.models import Buyer
from  .models import CustomerAddress

# Create your views here.


def checkout(request):
    user = Buyer.objects.get(user=request.user)
    if request.method == "POST":
        if request.method == "POST":
            address = CustomerAddress(
                buyer = user,
                country  = "India",
                full_name = request.POST.get('full_name', ''),
                mobile_number = request.POST.get('mobile_number', ''),
                pincode = request.POST.get('pincode', ''),
                address_line1 = request.POST.get('address_line1', ''),
                address_line2 = request.POST.get('address_line2', ''),
                state = request.POST.get('state', ''),
                city = request.POST.get('city', ''),
                
            )
            address.save()
            return redirect('checkout')  
        #  
    
    customerAddress  = CustomerAddress.objects.filter(buyer__user= request.user)
    context = {
        'customerAddress': customerAddress,

    }
    return render(request, 'checkout.html', context)
def paymentSuccess(request):
    return render(request, 'payment_successful.html')
