from django.db import models

# Create your models here.

class Customer(models.Model):
    image = models.ImageField(upload_to = 'customer_images/',blank=True)
    name = models.CharField(max_length=20)
    admission_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Customers'

class Order(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.IntegerField()
    phone = models.CharField(max_length=15,default='254111255419')
    total = models.FloatField()
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}--{self.phone}'
    
    class Meta:
        verbose_name_plural = 'Orders'