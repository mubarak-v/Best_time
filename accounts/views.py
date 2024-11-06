from django.contrib import messages  # Correct import
from django.shortcuts import redirect, render
from django.urls import path
from .form import LoginAsSellerForm, LoginAsBuyerForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt




# Create your views here.

# Login as Seller"

# Login as Buyer
# urls.py
from django.contrib.auth import views as auth_views
from django.contrib import messages


# @csrf_exempt
def seller(request):
    logins = False
    form = LoginAsSellerForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username = username,password = password)
            if user is not None and user.groups.filter(name = 'Sellers').exists():
                login(request, user)
                messages.success(request, "successfully logged ")
                logins = True
                return redirect('dashboard')
            
            else:
        
                messages.error(request,"invalid username or password")
    if 'next' in request.GET:
        messages.info(request, "Please log in as a seller to access the dashboard.")
    
    else:
        form =LoginAsSellerForm()
        logins = False


    return render(request, 'login_as_seller.html', {'form':form,'logins':logins})



def buyer(request):
    form = LoginAsBuyerForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():

            username  = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password = password)
            if user is not None and user.groups.filter(name = 'Buyers').exists():
                login(request, user)
                messages.success(request, "Successfully logged in")
                return redirect('home')
            
            else:
                messages.error(request, "Invalid username or password")
        else:
            form =LoginAsSellerForm()

    context ={
        'form': form,
    }    

    return render(request, 'login_as_buyer.html',context)


def custom_csrf_failure(request, reason=""):
    return HttpResponseForbidden("CSRF verification failed: " + reason)