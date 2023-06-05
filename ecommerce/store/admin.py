from django.contrib import admin

# Register your models here.
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display=['username','email','introduction']

class ProductImagesAdmin(admin.TabularInline):
    model=ProductImages

class ProdcutAdmin(admin.TabularInline):
    model=Product
class CategoryAdmin(admin.ModelAdmin):
    inlines=[ProdcutAdmin]
    list_display=['title','Category_image']


class ProdcutAdmin(admin.ModelAdmin):
    inlines=[ProductImagesAdmin]
    list_display=['name','user','Product_image','price','product_status','freature','digital']


class VendorAdmin(admin.ModelAdmin):
    list_display=['title','Vendor_image']

class OrderAdmin(admin.ModelAdmin):
    list_editable=['paid_status','product_status']
    list_display=['customer','date_order','paid_status','complete','transaction_id','product_status','get_cart_total']

class OrderItemAdmin(admin.ModelAdmin):
    list_display=['product','product_status','quantity','date_added','get_total']
    def get_total(self, obj):
        return obj.get_total
    get_total.short_description = 'Total'
    
admin.site.register(User,UserAdmin)
admin.site.register(Customer)
admin.site.register(Product,ProdcutAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(ShippingAddress)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Vendor,VendorAdmin)
admin.site.register(Tag)
admin.site.register(ProductReview)
admin.site.register(WishList)