from django.contrib import admin
from .models.product import Product
from .models.catagory import Catagory
from .models.customer import Customer
from .models.order import Order

class AdminProduct(admin.ModelAdmin):
    list_display = ["name" , "price" , "description" , "catagory"]
    
class AdminCatagory(admin.ModelAdmin):
    list_display = ["name"]
# Register your models here.
admin.site.register(Product, AdminProduct)
admin.site.register(Catagory, AdminCatagory)
admin.site.register(Customer)
admin.site.register(Order)
