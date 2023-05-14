from .models import *
from django.db.models import Max,Min


def default(request):
    categories=Category.objects.all()
    venders=Vendor.objects.all()
    tags=Product.tags.all()
    min_max_price=Product.objects.aggregate(Min('price'),Max('price'))
    
    
    # address=ShippingAddress.objects.get(user=request.user)
    return { 'categories':categories,
            'venders':venders ,
            'tags':tags,
            'min_max_price':min_max_price        
            }