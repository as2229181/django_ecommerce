import json
from .models import *

def cookeieCart(request):
    
    try:
        cart=json.loads(request.COOKIES['cart'])
    except:
        cart={}
    
    print('cart:',cart)
    items=[]
    order={"get_cart_items":0,"get_cart_total":0,'shipping':False}
    cartItems=order['get_cart_items']
    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            product=Product.objects.get(id=i)
            total=(product.price*cart[i]['quantity'])
            order['get_cart_total']+=total
            order['get_cart_items']=cartItems
            item ={
                'product':{
                'id':product.id,
                'name':product.name,
                'price':product.price,
                'imagURL':product.imagURL    
                },
                'quantity':cart[i]['quantity'],
                'get_total':total   
            }
            items.append(item)
            print(items)
            if product.digital==False:
                order['shipping']=True   
        except:
            pass     
    return {'items':items,"order":order,"cartItems":cartItems}


def cartData(request):
    
    customer=None

    if request.user.is_authenticated: #確認user是有被授權的
            user=request.user
            customer,created= Customer.objects.get_or_create(user=user,name=user.username,email=user.email) #獲得user作為customer的資料
            order,created=Order.objects.get_or_create(customer=customer,complete=False)#如果user還不是
            items=order.orderitem_set.all()
            cartItems=order.get_cart_items
    else:
       cookieData= cookeieCart(request)
       items=cookieData['items']
       order=cookieData['order']
       cartItems=cookieData['cartItems'] 
    return {'items':items,"order":order,"cartItems":cartItems}

def guestOrder(request,data):
    print('User is not logged in!!!')
    print('COOKIES:',request.COOKIES)
    name=data['form']['name']
    email=data['form']['email']
    cookieData=cookeieCart(request)
    items=cookieData['items']
    customer,created=Customer.objects.get_or_create(
        email=email
    )
    customer.name=name
    customer.save()
    order=Order.objects.create(
        customer=customer,
        complete= False,
    )
    for item in items:
        product=Product.objects.get(id=item['product']['id'])
        orderItem=OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer,order