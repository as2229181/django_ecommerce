from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .models import*
import json
import datetime
from .utils import cookeieCart,cartData,guestOrder
from .form import UserRegisterForm,ProductReviewForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.db.models import Count,Avg
from  taggit.models import Tag
from django.db.models import Q
from django.template.loader import render_to_string  
        
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

def test(request):
    return render(request,'new cart/about.html')
def test1(request):
    return render(request,'new cart/contact.html')


def test2(request):
    category=Category.objects.all()
    # category=Category.objects.all().annotate(product_count=Count('product'))
    context={
        'category':category
        
    }
    return render(request,'new cart/index.html',context)

def test3(request,sui):
    product=Product.objects.get(sui=sui)
    p_images=product.p_image.all()
    related_product=Product.objects.filter(category=product.category)
    reviews=ProductReview.objects.filter(product=product)
    average_rating=ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    review_form=ProductReviewForm()
   
    make_review=True
    if request.user.is_authenticated:
        user_review_count=ProductReview.objects.filter(user=request.user,product=product).count()
        if user_review_count>0:
            make_review=False
        
    # print(p_images)
    product_images=[]
    for p in p_images:
        product_images.append(p.image.url)
    print(product_images)  
    for index ,images in enumerate(product_images)  :
        print (index ,images)
    
    context={
        'product':product,
        'p_images':p_images,
        'reviews':reviews,
        'make_review':make_review,
        'review_form':review_form,
        'average_rating':average_rating,
        'product_images_enumerated':enumerate(product_images),
        'product_images':product_images,
        'related_product':related_product
            
    }
    return render(request,'new cart/shop-single.html',context)
def test4(request):
    product=Product.objects.all()
    category=Category.objects.all()
    data=cartData(request)
    items=data['items']
    order=data['order']
    cartItems=data['cartItems']  
    products=Product.objects.all()
    context={'word':'this is  store page',
             'Products':products,
             'order':order,
             "items":items,
             "cartItems":cartItems,
             'category':category}
    context={
        'products':product
        
    }
    return render(request,'new cart/shop.html',context)
def test5(request, cid):
    category=Category.objects.get(cid=cid)
    product=Product.objects.filter(category=category)
    context={
        'category':category,
        'product':product
        
    }
    return render(request,'new cart/category.html',context)

def test6(request):
    vendor=Vendor.objects.all()
    context={
        'vendor':vendor
    }
    return render(request,'new cart/vendor.html',context)

def test7(request,vid):
    vendor=Vendor.objects.get(vid=vid)
    products=Product.objects.filter(vendor=vendor)
    # category=Category.objects.filter(vendor=vendor)
    context={
        'vendor':vendor,
        'products':products
        
        
    }
    return render(request,'new cart/vendor-detail.html',context)


def test8(request,tag_slug=None):
    products=Product.objects.filter(product_status='published').order_by('-date')
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        products=products.filter(tags__in=[tag])
        context={
            'products':products     
        }
    return render(request,'new cart/tag_shop.html',context)

def ajax_add_review(request,sui):
    product=Product.objects.get(sui=sui)
    user=request.user
    review=ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating']
    )
    username=user.username
    print(username)
    
  
    
    context={
        'user':user.username,
        'review':request.POST['review'],
        'rating':request.POST['rating'],
        'date':review.date
    }
    average_rating=ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    return JsonResponse(
        {'bool': True,
        'context':context,
        'average_rating':average_rating

        } 
    )
    
def search_view(request):
    query= request.GET.get('q')
    products=Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)).order_by('-date')
    print(query)
    print(products)
    
    context={
        'products':products,
        'query':query        
    }
    return render(request,'new cart/search.html',context)

def filter_product(request):
    categories=request.GET.getlist('category[]')
    vendors=request.GET.getlist('vendor[]')
    tags=request.GET.getlist('tag[]')
    min_price=request.GET['min_price']
    max_price=request.GET['max_price']
    
    products=Product.objects.all().order_by('-id').distinct()
    products=products.filter(price__gte=min_price)
    products=products.filter(price__lte=max_price)
    
    
    print(categories)
    print(vendors)
    if len(categories) > 0 :
        products=products.filter(category__id__in=categories).distinct()
    if len(vendors) > 0 :
        products=products.filter(vendor__id__in=vendors).distinct()
    if len(tags) > 0 :
            products=products.filter(tags__id__in=tags).distinct()
        
    data= render_to_string("new cart/async/product-list.html",{"products":products})  
    
    return JsonResponse({"data":data})
        
     