
from django import forms
from .models import Seller


# class  Login_as_seller(forms.ModelForm):
#     class Meta:
#         model = Seller
#         fields = [ 'username','password']
#         widgets = {
#             'user': forms.CharField(attrs = {'class': 'form-control',''}),
#             'password': forms.PasswordInput(attrs = {'class': 'form-control'}),
#         }




class LoginAsSellerForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
class LoginAsBuyerForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
