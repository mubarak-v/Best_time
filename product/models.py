from django.db import models
from accounts.models import  Seller,Buyer

# Create your models here

"""
name,price,description,image,created_at,updated_at,product_id,offer_price,brand,Special Feature,Battery Capacity


"""

class Product(models.Model):
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE, related_name="products")
    name = models.CharField( null=False,max_length=250)
    price = models.DecimalField(null= False, decimal_places=2,max_digits=10)
    description = models.TextField(null = False,max_length=250)
    image = models.ImageField(upload_to='product_images/')
    # created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    # updated_at = models.DateTimeField(auto_now=True)      # Automatically update on each save

    product_id = models.AutoField(primary_key=True)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True)
    special_feature = models.CharField(null=True, blank=True,max_length=250)
    battery_capacity = models.CharField(null=True,max_length=150)

    def save(self, *args, **kwargs):
        if self.seller:
            self.brand = self.seller.company_name
        super().save(*args, **kwargs)      
    def __str__(self):
        name = f"{self.name}_{self.brand}"
        return name
       
class Review(models.Model):
    product  = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    rating = models.DecimalField(decimal_places=1,max_digits=2)
    comment = models.TextField(max_length=200, null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer_name}_{self.product.name}"
    
class Cart(models.Model):
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}_cart"
    @property
    def total_cart_price(self):
        return sum(item.total_price for item in self.cart_items.all())
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name}_{self.cart.user}"
    @property
    def total_price(self):
        return self.quantity * self.product.price
    

class OrderDetails(models.Model):
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='order_details')
    order_id = models.CharField(max_length=100, unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    

class OrderItem(models.Model):
    order = models.ForeignKey(OrderDetails, on_delete=models.CASCADE, related_name='order_items')   
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=250)
    quantity = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    # ---------------------- customer details ----------------
    full_name = models.CharField(max_length=100, null=False)
    mobile_number = models.CharField(max_length=15, null=False )
    address = models.CharField(max_length=250, null=False)

    







    
