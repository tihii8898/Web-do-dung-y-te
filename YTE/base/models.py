
from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Product(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200,null=False,blank=False)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    price = models.DecimalField(max_digits=20,decimal_places=2,null=False,blank=False)
    category = models.CharField(max_length=200,null=False,blank=False)
    countInStock = models.IntegerField(null=True,blank=True,default=0)
    createAt = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True,editable=False)
    
    def __str__(self) -> str:
        return str(self.name)
    


class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('onl', 'Online'),
        ('off','Pay when received'),
    ]
    
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    paymentMethod = models.CharField(max_length=200,null = True,blank=True)
    shippingPrice = models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True,default=30000)
    totalPrice = models.DecimalField(max_digits=20,decimal_places=2,null=True,blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False,null=True,blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(auto_now_add=False,null=True,blank=True)
    isConfirmed = models.BooleanField(default=False)
    confirmedAt = models.DateTimeField(auto_now=True,null=True,blank=True)
    createAt = models.DateTimeField(auto_now_add=True)
    
    id = models.AutoField(primary_key=True,editable=False)

    def __str__(self) -> str:
        return str(self.id)
    
    
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    price = models.DecimalField(max_digits=20,decimal_places=2,null=True,blank=True)
    name = models.CharField(max_length=200,null = True,blank=True)
    image = models.CharField(max_length=200,null = True,blank=True)
    count = models.IntegerField(default=1,blank=True)
    id = models.AutoField(primary_key=True,editable=False)
    
    def __str__(self) -> str:
        return str(self.name)
    
    
    
class ShippingAddress(models.Model):
    order = models.OneToOneField(Order,on_delete=models.CASCADE,null=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    city = models.CharField(max_length=200,null=True,blank=True)
    phoneNumber = models.CharField(max_length=11,null=True,blank=False)
    id = models.AutoField(primary_key=True,editable=False)
    
    
    def __str__(self) -> str:
        return str(self.id)