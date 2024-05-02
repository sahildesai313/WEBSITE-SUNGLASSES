from django.contrib import admin
from .models import Person, Product, Address, Card, Contact,Cart


class PersonAdmin(admin.ModelAdmin):
    list_display = ("username", "fullname", "email", "phone", "gender")


admin.site.register(Person, PersonAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "image", "price", "framecolour", "id", "gender","image")


admin.site.register(Product, ProductAdmin)


class addressdetilsAdmin(admin.ModelAdmin):
    list_display = ("locality", "address", "city", "state")


admin.site.register(Address, addressdetilsAdmin)


class cardAdmin(admin.ModelAdmin):
    list_display = ("cardname", "cardnumber", "cvv","MM", "YYYY")


admin.site.register(Card, cardAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "massage")


admin.site.register(Contact, ContactAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ("person","product","quantity")

admin.site.register(Cart,CartAdmin)
