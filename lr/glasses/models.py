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
    otp = models.CharField(max_length=4, null=True, blank=True)
    country = models.CharField(max_length=10, default="")

    def __str__(self):
        return f"{self.username} - {self.fullname} - {self.email} - {self.phone} - {self.gender} - {self.country}"


class GenderChoices(models.IntegerChoices):
    MALE = 1, "MALE"
    FEMALE = 2, "FEMALE"


class Address(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
    )
    locality = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    pincode = models.CharField(max_length=6)
    city = models.CharField(max_length=10)
    state = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.locality} - {self.address} - {self.pincode} - {self.city} - {self.state}"


class Card(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    cardname = models.CharField(max_length=250)
    cardnumber = models.CharField(max_length=100)
    MM = models.CharField(max_length=10)
    YYYY = models.CharField(max_length=10)
    cvv = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.cardname}"


class Contact(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    massage = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=250)
    price = models.IntegerField()
    modelnumber = models.CharField(max_length=10, default="")
    framesize = models.CharField(max_length=10, default="")
    framecolour = models.CharField(max_length=50, default="")
    framewidth = models.CharField(max_length=10, default="")
    image = models.ImageField(upload_to="image", default=None)
    id = models.AutoField(primary_key=True)
    gender = models.IntegerField(
        choices=GenderChoices.choices, default=GenderChoices.MALE
    )

    def __str__(self):
        return f"{self.id} - {self.name}"


class Cart(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
