# accounts/admin.py


from django.contrib import admin
from .models import Seller, Buyer

admin.site.register(Seller)
admin.site.register(Buyer)
