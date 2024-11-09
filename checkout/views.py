from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.models import Buyer
from  .models import CustomerAddress,CardData

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
    if request.method == "POST":
        address_id = request.POST.get('address', '')
        
        if address_id:
            print(f"Selected address ID: {address_id}")
        else:
            print("No address selected")
        
        # Render success page or redirect as needed
        return render(request, 'payment_successful.html')
    
    # Redirect or handle non-POST requests if necessary
    return redirect('checkout')