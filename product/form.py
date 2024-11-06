from django import forms
from .models import Product, Review

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields =  [
            'name', 
            'price', 
            'description', 
            'image', 
            'offer_price', 
            
            'special_feature', 
            'battery_capacity'
        ]
        widgets = {
            'name': forms.TextInput(attrs ={'class': 'form-control'}),
            'price': forms.NumberInput(attrs ={'class': 'form-control'}),
            'description':forms.Textarea(attrs ={'rows':4}),
            'image': forms.FileInput(attrs = {'class': 'form-control'}),
            'offer_price': forms.NumberInput(attrs ={'class': 'form-control'}),
            'special_feature': forms.TextInput(attrs ={'class': 'form-control'}),
            'battery_capacity': forms.TextInput(attrs ={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields =['rating','comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),   
            'comment':forms.TextInput(attrs={'class': 'form-control'}),
        }