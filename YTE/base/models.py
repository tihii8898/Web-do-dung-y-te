
from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Product(models.Model):
    """
    Model chứa các sản phẩm của cửa hàng
    Với các thông số khởi tạo bắt buộc: name, price, category

    
    """
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
        """
        Trả về name của object
        """
        return str(self.name)
    


class Order(models.Model):
    """
    Model chứa các đơn hàng của khách hàng, một khách hàng sẽ có thể có nhiều đơn hàng khác nhau, đơn hàng mặc định được khởi tạo mỗi khi khách hàng cho thêm hàng vào giỏ. Và mặc định đơn hàng chưa tiến hành đặt hàng sẽ ở trạng thái chưa thanh toán.
    
    """
    
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
        """
        Hiển thị id của đơn hàng
        """
        return str(self.id)
    
    
    
class OrderItem(models.Model):
    """
    Model chứa các sản phẩm được khách hàng cho vào giỏ hàng. Mỗi mặt hàng được đặt sẽ thuộc về một đơn hàng duy nhất và một khách hàng duy nhất. Sau khi đơn hàng được thanh toán, đặt hàng thì mặt hàng sẽ bị xóa khỏi database. 
    """
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    price = models.DecimalField(max_digits=20,decimal_places=2,null=True,blank=True)
    name = models.CharField(max_length=200,null = True,blank=True)
    image = models.CharField(max_length=200,null = True,blank=True)
    count = models.IntegerField(default=1,blank=True)
    id = models.AutoField(primary_key=True,editable=False)
    
    def __str__(self) -> str:
        """
        Hiển thị tên của mặt hàng được đặt
        """
        return str(self.name)
    
    
    
class ShippingAddress(models.Model):
    """
    Model chứa dữ liệu vị trí nhận hàng của khách hàng. Mỗi đơn hàng sẽ có duy nhất một địa chỉ nhận hàng. 
    """
    order = models.OneToOneField(Order,on_delete=models.CASCADE,null=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    city = models.CharField(max_length=200,null=True,blank=True)
    phoneNumber = models.CharField(max_length=11,null=True,blank=False)
    id = models.AutoField(primary_key=True,editable=False)
    
    
    def __str__(self) -> str:
        """
        Hiển thị id của địa chỉ nhận hàng
        """
        return str(self.id)