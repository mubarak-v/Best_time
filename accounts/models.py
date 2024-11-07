from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# username:dude
# password:dude
#username:mubarak
# password:mubarak

"""

"""
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    address  = models.CharField( max_length=250)
    contact_number = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_created = True)
    

    def __str__(self):
        username = f"{self.company_name}_{self.user.username}"
        return username
    


class Buyer(models.Model):
        user = models.OneToOneField(User,on_delete=models.CASCADE)
        address = models.CharField(max_length=250, null=True)
        contact_number = models.CharField(max_length=12, null = True)
        

        def __str__(self):
            username = self.user.username
            return username    