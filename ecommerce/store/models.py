from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe 
 
 
def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id,filename)


STATUS_CHOICE=(
    ('process','Processing'),
    ('shipped','Shipped'),
    ('deliered','Deliered'),    
)

STATUS=(
    ('draft','Draft'),
    ('disabled','Disabled'),
    ('rejected','Rejected'),
     ('in_review','In_Reiview'),
     ('published','Published'),   
)


RATING=(
    ('1','★✰✰✰✰'),
    ('2','★★✰✰✰'),
    ('3','★★★✰✰'),
    ('4','★★★★✰'),
    ('5','★★★★★'),   
)






# Create your models here.
class User(AbstractUser):
    username=models.CharField(max_length=200, null=False,blank=True)
    email= models.EmailField(unique=True)
    introduction=models.CharField(max_length=2000)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    
    def __str__(self):
        return self.username
        
        
class Category(models.Model):
    cid=ShortUUIDField(unique=True, length=10, max_length=20, prefix='cat', alphabet='abcdefghijkl1234567890')       
    title=models.CharField(max_length=100)
    image=models.ImageField (upload_to='category') 
     
    class Meta:
        verbose_name_plural='Categories'
    @property
    def imagURL(self):
        try:
            url=self.image.url
        except:
            url=""
        return url
    def __str__(self):
        return self.title
class vendor(models.Model):
    vid=ShortUUIDField(unique=True, length=10 , max_length=20, prefix='ven', alphabet='abcdefghijkl1234567890'  )
    title=models.CharField(max_length=1000)
    image=models.ImageField(upload_to=user_directory_path())
    descripton=models.TextField(null=True , blank=True)
    
    address=models.CharField(max_length='100',default='123,main,street')
    contact=models.CharField(max_length='100',default='+886 0912768057')
    #chat response time
    chat_resp_time=models.CharField(max_length='100',default='1')
    shipp_ontime=models.CharField(max_lenth='100',default='100')
    authentic_rating=models.CharField(max_length='100',default='100')
    days_return=models.CharField(max_length='100',default='100')
    warrant_period=models.CharField(max_length='100',default='100')
    
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    class Meta:
        verbose_name_plural='Vendors'
    @property
    def imagURL(self):
        try:
            url=self.image.url
        except:
            url=""
        return url
    def __str__(self):
        return self.title

      
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.name or ''

class Tag(models.Model):
    pass
        
class Product(models.Model):
    
    name=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    
    price=models.DecimalField(max_digits=7,decimal_places=2)
    old_price=models.DecimalField(max_digits=7,decimal_places=2)
    tag=models.ForeignKey(Tag,on_delete=models.SET_NULL,null=True,blank=True)
    
    
    product_status=models.CharField(choices=STATUS,max_length=10, default='in_review')
    
    status=models.BooleanField(default=True)
    in_stock=models.BooleanField(default=True)
    freature=models.BooleanField(default=False)
    digital=models.BooleanField(default=False,null=True,blank=False) #判斷是不是實體的東西所以要不要運送
    
    image =models.ImageField(null=True,blank=True) 
    def __str__(self):
        return self.name
    @property
    def imagURL(self):
        try:
            url=self.image.url
        except:
            url=""
        return url

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_order=models.DateField(auto_now_add=True)
    complete=models.BooleanField(default=False,null=True,blank=False)
    transaction_id=models.CharField(max_length=200,null=True)
    def __str__(self):
        return str(self.id)
    @property
    def shipping(self):
        shipping=False
        orderitems=self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital==False:
                shipping=True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()#把customer所有產品定單資訊都拿出來
        total=sum([ item.get_total  for item in orderitems ])#利用for loop 把每個產品訂單的total都算出來在加總
        return total
    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()#把customer所有產品定單資訊都拿出來
        total=sum([ item.quantity  for item in orderitems ])#利用for loop 把每個產品訂單的數量都算出來在加總
        return total
        
class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total=self.product.price*self.quantity
        return total
   
class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address=models.CharField(max_length=200,null=False)
    city=models.CharField(max_length=200,null=False)
    state=models.CharField(max_length=200,null=False)
    zipcode=models.CharField(max_length=200,null=True)
    date_add=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address