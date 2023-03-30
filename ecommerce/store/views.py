from django.shortcuts import render
from .models import*
# Create your views here.
def store(request):
    products=Product.objects.all()
    context={'word':'this is  store page',
             'Products':products}
    return render(request,"Store.html",context)
def cart(request):
    customer=None
    if request.user.is_authenticated: #確認user是有被授權的
        try:
            customer= request.user.customer #獲得user作為customer的資料
        except Customer.DoesNotExist:
            pass
        if customer  is not None:
            order,created=Order.objects.get_or_create(customer=customer,complete=False)#如果user還不是
            items=order.orderitem_set.all()
        else:
            items=[]
            order={"get_cart_items":0,"get_cart_total":0}
    context={'items':items,"order":order}
    return render(request,"Cart.html",context)
def checkout(request):
    customer=None
    if request.user.is_authenticated: #確認user是有被授權的
        try:
            customer= request.user.customer #獲得user作為customer的資料
        except Customer.DoesNotExist:
            pass
        if customer  is not None:
            order,created=Order.objects.get_or_create(customer=customer,complete=False)#如果user還不是
            items=order.orderitem_set.all()
        else:
            items=[]
            order={"get_cart_items":0,"get_cart_total":0}
    context={'items':items,"order":order}
    return render(request,"Checkout.html",context)


