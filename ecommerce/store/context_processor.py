from .models import *
from django.db.models import Max,Min
from django.contrib import messages

def default(request):
    categories=Category.objects.all()
    venders=Vendor.objects.all()
    tags=Product.tags.all()
    min_max_price=Product.objects.aggregate(Min('price'),Max('price'))
    
    try:
        customer=Customer.objects.get(user=request.user)
    except:
        pass
    try:
        total_count=WishList.objects.filter(customer=customer).count()
    except:
        messages.warning(request,'You need to login before accessing yor wishlist!!')
        total_count=0

    try:
        address=ShippingAddress.objects.filter(customer=customer).first()
        print(address)
    except:
        address=None
        print(address)
    # address=ShippingAddress.objects.get(user=request.user)
    return { 'categories':categories,
            'venders':venders ,
            'tags':tags,
            'min_max_price':min_max_price,
            'total_count':total_count,
            'address':address,
                  
            }