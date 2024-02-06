from django.db import models

# Create your models here.

from django.db import models

class person(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    username = models.CharField(max_length=150, unique=True)
    fullname = models.CharField(max_length=150, default="")
    email = models.EmailField(default="")
    phone = models.CharField(max_length=10, default="")  
    password = models.CharField(max_length=100, default="")
    confirmpassword = models.CharField(max_length=100, default="")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="")
    otp=models.CharField(max_length=4,default='', null=True, blank=True)
    country = models.CharField(max_length=10,default="")

    def __str__(self):
        return f"{self.username} {self.fullname} {self.email} {self.phone} {self.gender} {self.country}"




class product(models.Model):
    product_name=models.CharField(max_length=250)
    product_price=models.IntegerField()
    product_description =models.TextField(max_length=250)
    product_image=models.ImageField(upload_to="food",default=None)
    id=models.AutoField(primary_key=True)
    

    def __str__(self):
        return f"{self.product_name}{self.product_price}{self.product_description}{self.product_image}{self.id}"