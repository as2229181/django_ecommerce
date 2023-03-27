from django.shortcuts import render
from .models import*
# Create your views here.
def store(request):
    products=Product.objects.all()
    context={'word':'this is  store page',
             'Products':products}
    return render(request,"Store.html",context)
def cart(request):
    context={'word':'this is cart page'}
    return render(request,"Cart.html",context)
def checkout(request):
    context={'word':'this is chechout page'}
    return render(request,"Checkout.html",context)


