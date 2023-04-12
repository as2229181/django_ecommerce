from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import*
import json
import datetime
from .utils import cookeieCart,cartData,guestOrder
from .form import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.conf import settings
# Create your views here.
User=get_user_model()
def register(request):
    if request.method =='POST':     
        form=UserRegisterForm(request.POST)
        print(form)
        try:
            if form.is_valid:
                new_user=form.save()
                username=form.cleaned_data.get('username')
                print(username)
                messages.success(request,f'{username},Your account was created successfully!!!')            
                new_user=authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['passwrod1'],
                                    
                                    )
                login(request,new_user)         
            print('User registered successfully!')
        except Exception as e:
            message=messages.error(request, f'Error: {str(e)}')
        return redirect('/store/')
    else:
        form=UserRegisterForm()
        print('User cannot be registered!')    
    
    context={'form':form}
    return render(request,'userauths/Signup.html',context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request,f'Hey you are already loggin!!')
        return redirect('store')
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user=User.objects.get(email=email)
            print(user.email)
            user=authenticate(request,email=email,password=password)
            if user is not None:            
                login(request,user)
                messages.success(request,"Logged in successfully!!!")
                return redirect ('store')
            else:
                messages.warning(request,'User is no exist,cret one!!!')
        except:
            messages.warning(request,f'User with {email} does not exist!!!')
       
    context={}        
    return render(request,'userauths/Signin.html',context)

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'You logged out!') 
        return redirect('/store/login/')
    else:
        messages.warning(request,'You are not logged in!!')
        return redirect('/store/login/')
def store(request):
    data=cartData(request)
    items=data['items']
    order=data['order']
    cartItems=data['cartItems']  
    products=Product.objects.all()
    context={'word':'this is  store page',
             'Products':products,
             'order':order,
             "items":items,
             "cartItems":cartItems}
    return render (request,"Store.html",context)
def cart(request):
    # items=[]
    # order=[]
    # cartItems=[]
    data=cartData(request)
    items=data['items']
    order=data['order']
    cartItems=data['cartItems']    
    context={'items':items,"order":order,"cartItems":cartItems}
    return render(request,"Cart.html",context)
def checkout(request):
    data=cartData(request)
    items=data['items']
    order=data['order']
    cartItems=data['cartItems'] 
    context={'items':items,"order":order,"cartItems":cartItems}
    return render(request,"Checkout.html",context)

def updateItem(request):
    data=json.loads(request.body)
    productId = data['productId']
    action=data['action']
    
    
    print('Action:',action)
    print('productId:',productId)
    
    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created=OrderItem.objects.get_or_create(product=product,order=order)
    
    if action=="add":
        orderItem.quantity=(orderItem.quantity+1)
    elif action=="remove":
        orderItem.quantity=(orderItem.quantity-1)
    orderItem.save() 
    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse("Item wsa added!!", safe=False)

def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        
    else:
        customer,order=guestOrder(request,data)
        
    total=float(data['form']['total'])
    order.transaction_id=transaction_id
    if total == float(order.get_cart_total):
        order.complete=True
        order.save()
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],  
            )    
    return JsonResponse('Payment completed',safe=False)

