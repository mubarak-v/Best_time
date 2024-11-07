from django.contrib import messages 
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .form import  LoginAsBuyerForm, userRegistrationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from django.contrib import messages
from .models import Buyer



def buyer(request):
    user_type = request.GET.get('user_type')
    if request.method == 'POST':
        if user_type == 'buyer':
            form = LoginAsBuyerForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None and user.groups.filter(name='Buyers').exists():
                    login(request, user)
                    messages.success(request, "Successfully logged in")
                    return redirect('home')
                else:
                    messages.error(request, "Invalid username or password or you don't have Buyer access")        
        else:
            form = LoginAsBuyerForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None and user.groups.filter(name='Sellers').exists():
                    login(request, user)
                    messages.success(request, "Successfully logged in")
                    return redirect('dashboard')
                else:
                    messages.error(request, "Invalid username or password ")
    
    else:
        form = LoginAsBuyerForm()
    context = {
        'form': form,    
    }
    return render(request, 'login.html', context)

def custom_csrf_failure(request, reason=""):
    return HttpResponseForbidden("CSRF verification failed: " + reason)


def useRegistration(request):
    user_type = request.GET.get('user_type')
    if request.method == "POST" and user_type == "buyer":    
            form = userRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)  # Log the user in after successful registration
                return redirect('home')
            else:
                # Handle form errors by redisplaying the form with errors
                return render(request, 'registration.html', {'form': form})
    else:
        form = userRegistrationForm()
    return render(request, 'registration.html',  {'form': form})

        
        





