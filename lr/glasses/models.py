from django.db import models

class Person(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    username = models.CharField(max_length=150)
    fullname = models.CharField(max_length=150, default="")
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=8)
    confirmpassword = models.CharField(max_length=8)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="")
    otp = models.CharField(max_length=4,null=True, blank=True)
    country = models.CharField( max_length=10, default="")

    def __str__(self):
        return f"{self.username} {self.fullname} {self.email} {self.phone} {self.gender} {self.country}"


class GenderChoices(models.IntegerChoices):
    MALE = 1, "MALE"
    FEMALE = 2, "FEMALE"
    UNKNOWN = 0, "UNKNOWN"


class Product(models.Model):
    name = models.CharField(max_length=250)
    price = models.IntegerField()
    modelnumber=models.CharField(max_length=10,default='')
    framesize = models.CharField(max_length=10, default='')
    framecolour = models.CharField(max_length=10, default='')
    framewidth=models.CharField(max_length=10, default='')
    image = models.ImageField(upload_to="food", default=None)
    id = models.AutoField(primary_key=True)
    gender = models.IntegerField(choices=GenderChoices.choices, default=GenderChoices.UNKNOWN)

    def __str__(self):  
        return f"{self.id} - {self.name}"


class Address(models.Model):
    person = models.ForeignKey(Person, on_delete = models.CASCADE,)
    locality = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    pincode = models.CharField(max_length=6)
    city = models.CharField(max_length=10)
    state = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.locality} {self.address} {self.pincode} {self.city} {self.state}"


class Card(models.Model):
    address = models.ForeignKey(Address, on_delete = models.CASCADE, default='')
    nameoncard=models.CharField(max_length=250)
    cardno=models.CharField(max_length=12)
    date=models.DateField()
    cvv=models.IntegerField()

    def __str__(self):
        return f"{self.nameoncard}"


