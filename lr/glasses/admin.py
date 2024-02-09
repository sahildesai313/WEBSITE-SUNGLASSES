from django.contrib import admin
from .models import *

class personAdmin(admin.ModelAdmin):
    list_display = ("username","fullname","email","phone","gender",)
admin.site.register(person, personAdmin)



class productAdmin(admin.ModelAdmin):
    list_display = ("product_name","product_price","product_description","product_image")
admin.site.register(product, productAdmin)


class maleproductAdmin(admin.ModelAdmin):
    list_display = ("product_name","product_price","product_description","product_image")
admin.site.register(maleproduct, maleproductAdmin)

class femaleproductAdmin(admin.ModelAdmin):
    list_display = ("product_name","product_price","product_description","product_image")
admin.site.register(femaleproduct, femaleproductAdmin)