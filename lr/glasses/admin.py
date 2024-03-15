from django.contrib import admin
from .models import Person, Product, Address, Card


class PersonAdmin(admin.ModelAdmin):
    list_display = ("username", "fullname", "email", "phone", "gender")
admin.site.register(Person, PersonAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price",  "framesize", "framecolour", "framewidth", "image", "id", "gender")
admin.site.register(Product, ProductAdmin)


class addressdetilsAdmin(admin.ModelAdmin):
    list_display = ("locality", "address", "city", "state")
admin.site.register(Address, addressdetilsAdmin)


class cardAdmin(admin.ModelAdmin):
    list_display = ("nameoncard", "cardno", "date", "cvv")
admin.site.register(Card, cardAdmin)
