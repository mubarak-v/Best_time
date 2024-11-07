
from django import forms
from .models import Buyer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginAsSellerForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
from django import forms
class LoginAsBuyerForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'placeholder': 'Enter your username',
            'required': 'required'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password',
            'placeholder': 'Enter your password',
            'required': 'required'
        })
    )
class userRegistrationForm(UserCreationForm):
    class Meta :
        model = User
        fields = ['username',  'password1', 'password2']
    def save(self, commit=True):
        user = super().save(commit=commit)
        Buyer.objects.create(user=user, contact_number=None, address=None)
        return user


