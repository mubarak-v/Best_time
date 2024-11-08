from django.db import models

from accounts.models import Buyer

# Create your models here.

class CustomerAddress(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='addresses')
    country = models.CharField(max_length=100, null=False)
    full_name = models.CharField(max_length=50, null= False)
    mobile_number = models.CharField(max_length=15, null=False)
    pincode = models.CharField(max_length=10, null=False)
    address_line1 = models.CharField(max_length=100, null=False)
    address_line2 = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=50, null=False)
    id_default= models.BooleanField(default=False)
    city = models.CharField(max_length=50, null=False)


    
