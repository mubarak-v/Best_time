from django.contrib import admin

# Register your models here.
from .models import Product
from .models import Review,CartItem,Cart


admin.site.register(Product)
admin.site.register(Review)
admin.site.register(CartItem)
admin.site.register(Cart)