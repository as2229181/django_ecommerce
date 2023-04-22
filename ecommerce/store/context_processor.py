from .models import *



def default(request):
    categories=Category.objects.all()
    address=ShippingAddress.objects.get(user=request.user)
    return { 'categories':categories,"address":address}