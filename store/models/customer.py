from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=500)
    
    def isExist(self):
        if Customer.objects.filter(email = self.email):
            return True
        return False
    
    def register(self):
        self.save()
      
    @staticmethod  
    def get_customer_by_email(email):
      return Customer.objects.get(email = email)
