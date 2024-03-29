from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.utils.text import slugify
from os.path import splitext
def user_directory_path(instance,filename):
    name, ext = splitext(filename)
    slugified_name = slugify(name)
    # 重新組合檔名和副檔名
    filename = "{}{}".format(slugified_name, ext)
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
    ('', 'Chose the score'),
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

    def product_count(self):
        count=self.category.product.all()
        counts=sum([product.get_total for product in count])
        return counts

    def Category_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' %(self.image.url))

    @property
    def imagURL(self):
        try:
            url=self.image.url
        except:
            url=""
        return url
    def __str__(self):
        return self.title
class Vendor(models.Model):
    vid=ShortUUIDField(unique=True, length=10 , max_length=20, prefix='ven', alphabet='abcdefghijkl1234567890'  )
    title=models.CharField(max_length=1000)
    image=models.ImageField(upload_to=user_directory_path,default='user.jpg')
    # descripton=models.TextField(null=True , blank=True)
    descripton=RichTextField(null=True , blank=True)
    date=models.DateTimeField(null=True,blank=True)
    address=models.CharField(max_length=100,default='123,main,street')
    contact=models.CharField(max_length=100,default='+886 0912768057')
    #chat response time
    chat_resp_time=models.CharField(max_length=100,default='1')
    shipp_ontime=models.CharField(max_length=100,default='100')
    authentic_rating=models.CharField(max_length=100,default='100')
    days_return=models.CharField(max_length=100,default='100')
    warrant_period=models.CharField(max_length=100,default='100')

    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    class Meta:
        verbose_name_plural='Vendors'
    def Vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' %(self.image.url))
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
    contact=models.CharField(max_length=100,default='+886 0912768057')
    iamge = models.ImageField(upload_to=user_directory_path,default='user.jpg')
    def __str__(self):
        return self.name or ''
    @property
    def imagURL(self):
        try:
            url=self.image.url
        except:
            url=""
        return url


######################################Product###############################################
class Product(models.Model):

    name=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name='product')
    vendor=models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True,related_name='vendor')
    # description= models.TextField(null=True,blank=True,default='This is product!!!')
    description= RichTextField(null=True,blank=True,default='This is product!!!')
    price=models.DecimalField(max_digits=7,decimal_places=2)
    old_price=models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    specifications=models.TextField(null=True,blank=True )
    tags=TaggableManager(blank=True)
    stock_count=models.IntegerField(null=True,blank=True,default=100)

    product_status=models.CharField(choices=STATUS,max_length=10, default='in_review')

    status=models.BooleanField(default=True)
    in_stock=models.BooleanField(default=True)
    freature=models.BooleanField(default=False)
    digital=models.BooleanField(default=False,null=True,blank=False) #判斷是不是實體的東西所以要不要運送

    sui=ShortUUIDField(unique=True,length=4 ,max_length=10,prefix='sui',alphabet='1234567890' )
    date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated=models.DateTimeField(null=True,blank=True)

    image =models.ImageField(upload_to=user_directory_path,default='product.png')


    class Meta:
        verbose_name_plural='Products'
    def Product_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    @property
    def imagURL(self):
        try:
            url=self.image.url
        except:
            url=""
        return url
    def get_percentage(self):
        p_percentage=(self.price/self.old_price)*100
        return  p_percentage
    def __str__(self):
        return self.name

class ProductImages(models.Model):
    image=models.ImageField(upload_to='images',default='product.png')
    product=models.ForeignKey(Product,related_name='p_image',on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural='ProductImages'
    @property
    def imagURL(self):
        try:
            url=self.image.url
        except:
            url=""
        return url
 ################################Product###################################################


################################## Cart,OrderItems,Address#################################
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True,related_name='customer_order')
    date_order=models.DateField(auto_now_add=True)
    paid_status=models.BooleanField(default=False)
    complete=models.BooleanField(default=False,null=True,blank=False)
    product_status=models.CharField(choices=STATUS_CHOICE,max_length=33,default='processing')
    transaction_id=models.CharField(max_length=200,null=True)

    @property
    def shipping(self):
        shipping=False
        orderitems=self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital==False:
                shipping=True
        return shipping

    class Meta:
        verbose_name_plural='Orders'

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
    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    product_status=models.CharField(max_length=200,default='ok',null=True,blank=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=False)
    total=models.DecimalField(max_digits=7,decimal_places=2,default=0)
    class Meta:
        verbose_name_plural='Cart order items'
    def Order_image(self):
        return mark_safe('<img src="/images/&s" width="50" height="50"/>' %(self.image))
    @property
    def get_total(self):
        total=self.product.price*self.quantity
        return total

class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,related_name='address')
    address=models.CharField(max_length=200,null=False)
    city=models.CharField(max_length=200,null=False)
    state=models.CharField(max_length=200,null=False)
    zipcode=models.CharField(max_length=200,null=True)
    date_add=models.DateTimeField(auto_now_add=True)
    country=models.CharField(max_length=200,null=True,default='')
    status=models.BooleanField(default=False)
    class Meta:
        verbose_name_plural='Shipping address'
    def __str__(self):
        return self.address

################################## Product Review,wishlist,Address#################################
################################## Product Review,wishlist,Address#################################
################################## Product Review,wishlist,Address#################################
class ProductReview(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,related_name='review')
    review=models.TextField()
    rating=models.CharField(max_length=1,choices=RATING,default=None)
    date=models.DateField(auto_now_add=True)
    class Meta:
        verbose_name_plural='ProductReviews'

    def __str__(self):
        return self.product.name

    def get_rating(self):
        return self.rating



class WishList(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    date=models.DateField(auto_now_add=True)
    class Meta:
        verbose_name_plural='Wish List'

    def __str__(self):
        return self.product.name

class ContactUs(models.Model):
    full_name = models.CharField(max_length=200,null=True,blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField()


    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'
    def __str__(self):
        return self.full_name
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path,default='product.png')
    full_name = models.CharField(max_length=200, null=True, blank=True)
    introduction = models.CharField(max_length=200, null=True, blank=True)
    phone= models.CharField(max_length=200)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    @property
    def imagURL(self):
        try:
            url=self.image.url
        except:
            url=""
        return url

def create_userprofile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        pass
post_save.connect(create_userprofile, sender=User)
post_save.connect(save_user_profile, sender=User)