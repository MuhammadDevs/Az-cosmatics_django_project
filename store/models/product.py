from django.db import models
from .catagory import Catagory
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length= 255)
    price = models.IntegerField(default=0)
    catagory = models.ForeignKey(Catagory , default=1 , on_delete=models.CASCADE)
    description = models.CharField(max_length=255, default= '')
    image = models.ImageField(upload_to='uploads/products/')
    
    @staticmethod
    def get_all_products_by_catagory_id(catagory_id):
     if catagory_id:
        return Product.objects.filter(catagory_id=catagory_id)
    
    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in = ids)
