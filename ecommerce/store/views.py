from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse
from .models import*
import json
import datetime
from .utils import cookeieCart,cartData,guestOrder,del_wishlist
from .form import UserRegisterForm,ProductReviewForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Avg
from  taggit.models import Tag
from django.db.models import Q
from django.template.loader import render_to_string  
import logging
from .sample_create_order_ALL import main
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm



'''
Setting logger in views.py
'''
Logger = logging.getLogger('django')
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
        return redirect('test4')
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
                return redirect ('test4')
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
    
    
   
    filter=True
    products=Product.objects.all()
    context={'word':'this is  store page',
             'Products':products,
             
             
             'category':category}
    context={
        'products':product,
        'filter':filter,
        
    }
    return render(request,'new cart/shop.html',context)
def test5(request, cid):
    filter=False
    category=Category.objects.get(cid=cid)
    product=Product.objects.filter(category=category)
    context={
        'category':category,
        'product':product,
        'filter':  filter
    }
    return render(request,'new cart/category.html',context)

def vendor_view(request):
    vendor=Vendor.objects.all()
    context={
        'vendor':vendor
    }
    return render(request,'new cart/vendor.html',context)

def vender_detail(request,vid):
    vendor=Vendor.objects.get(vid=vid)
    products=Product.objects.filter(vendor=vendor)
    # category=Category.objects.filter(vendor=vendor)
    context={
        'vendor':vendor,
        'products':products
        
        
    }
    return render(request,'new cart/vendor-detail.html',context)


def customer_view(request):
    customers=Customer.objects.all()
    
    context={
        'customers':customers
    }
    return render(request,'new cart/customer.html',context)

def customer_detail(request,c_id):
    customer=Customer.objects.get(id=c_id)
    addresses= ShippingAddress.objects.filter(customer=customer).all().order_by('date_add')
    address_now=addresses.first()
    orders=Order.objects.filter(customer=customer).all().order_by('-date_order')
    if request.method == 'POST':
        address=request.POST.get('address')
        city=request.POST.get('city')
        state=request.POST.get('state')
        zipcode=request.POST.get('zipcode')
        state=request.POST.get('country')
        new_adddress=ShippingAddress.objects.create(customer=customer,address=address,city=city,state=state,zipcode=zipcode)
        messages.success(request,"Added Address successfully!!")
        customer_id=customer.id
        return redirect('customer_detail',customer_id)
    context={
        'customer':customer,
        'orders':orders,
        'addresses':addresses,
        'address_now':address_now
    }
    return render(request,'new cart/customer_detail.html',context)
 

def test8(request,tag_slug=None):
    products=Product.objects.filter(product_status='published').order_by('-date')
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        products=products.filter(tags__in=[tag])
        context={
            'products':products, 
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
        
def add_to_cart(request):
    cart_product={}
    totalcaritems=0
    cart_product[str(request.GET['id'])]={
        'name':request.GET['name'],
        'price':request.GET['price'],
        'quantity':request.GET['quantity'],
        'pid':request.GET['pid'],
        'product_image':request.GET['product_image'],
        'total_price':''
    }
    print(cart_product)
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['quantity'] = int(cart_product[str(request.GET['id'])]['quantity']) + int(cart_data[str(request.GET['id'])]['quantity'])
            cart_data.update(cart_data)

            cart_data[str(request.GET['id'])]['total_price'] = float(cart_data[str(request.GET['id'])]['price']) * int(cart_data[str(request.GET['id'])]['quantity'])
            cart_data.update(cart_data)
            request.session["cart_data_obj"] = cart_data
            totalcaritems=len(request.session['cart_data_obj'])
            del_wishlist(request,request.GET['id'])
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            cart_data[str(request.GET['id'])]['total_price'] = float(cart_data[str(request.GET['id'])]['price']) * int(cart_data[str(request.GET['id'])]['quantity'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
            totalcaritems=len(request.session['cart_data_obj'])
            del_wishlist(request,request.GET['id'])
    else:
        cart_product[str(request.GET['id'])]['total_price']= int(cart_product[str(request.GET['id'])]['quantity'])*float(cart_product[str(request.GET['id'])]['price'])
        request.session['cart_data_obj']= cart_product
        totalcaritems=len(request.session['cart_data_obj'])
        del_wishlist(request,request.GET['id'])
    
    print(totalcaritems)
    
    return JsonResponse({'data':request.session["cart_data_obj"],'totalcaritems':totalcaritems})


def cart_view(request):
    cart_total_amount = 0
    cart_data =request.session['cart_data_obj']
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['quantity'])*float(item['price'])            
            cart_data[p_id]['total_price']=round(int(cart_data[p_id]['quantity'])*float(cart_data[p_id]['price']), 2)
        request.session['cart_product_obj'] =cart_data
        request.session.modified = True  # 更新 session 中的資料
        request.session.save()  # 儲存 session 變更  
        context={'cart_data':cart_data,'totalcaritems':len(request.session['cart_data_obj']),'cart_total_account':cart_total_amount,}
        print (request.session['cart_data_obj']) 
        print (len(request.session['cart_data_obj']))
        return render(request,'new cart/Cart.html',context)
    else:
        messages.warning(request,'Your cart is empty!!')
        print('not in')
        return  redirect("test4")
    

def delete_from_cart(request):
    product_id=str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data=request.session['cart_data_obj']
            del cart_data[product_id]
            request.session['cart_product_obj'] =cart_data
            request.session.modified = True  # 更新 session 中的資料
            request.session.save()  # 儲存 session 變更
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['quantity'])*float(item['price'])
            cart_total_amount = round(cart_total_amount, 2)   
    context= render_to_string('new cart/async/cart-list.html',{'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})           
    return JsonResponse({'data':context,'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})


def update_cart(request):
    
    product_id=str(request.GET['id'])
    product_quantity = request.GET['quantity']
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data=request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['quantity']=product_quantity
            request.session['cart_product_obj'] =cart_data
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['quantity'])*float(item['price'])  
    context= render_to_string('new cart/async/cart-list.html',{'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})           
    return JsonResponse({'data':context,'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})


def change_cart_quantity(request):
    product_id=str(request.GET['id'])
    action= str(request.GET['action'])    
    cart_data=request.session['cart_data_obj']
    quantity=int(cart_data[product_id]['quantity'])
    if 'cart_data_obj'in request.session:
        if action == 'add':
            quantity+=1
            cart_data[product_id]['quantity']=str(quantity)
            product_sum = round(int(cart_data[product_id]['quantity'])*float(cart_data[product_id]['price']), 2)                      
            cart_data[product_id]['total_price']=product_sum
        if action == 'remove':
            quantity-=1
            cart_data[product_id]['quantity']=str(quantity)
            product_sum = round(int(cart_data[product_id]['quantity'])*float(cart_data[product_id]['price']), 2)  
            cart_data[product_id]['total_price']=product_sum
            if  quantity<=0:
                del cart_data[product_id]    
    request.session['cart_product_obj'] =cart_data
    request.session.modified = True  # 更新 session 中的資料
    request.session.save()  # 儲存 session 變更  
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['quantity'])*float(item['price'])
            cart_total_amount = round(cart_total_amount, 2)
               
    context= render_to_string('new cart/async/cart-list.html',{'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    
    return JsonResponse({'data':context,'quantity':quantity,'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount,'product_sum':product_sum})

@login_required
def checkout_view(request):

    host=request.get_host()
    print(host)
    paypal_dict={
         'business':settings.PAYPAL_RECEIVER_EMAIL,
         'amount':200,
         'item_name':'Order-Item-NO-3',
         'currency_code':'USD',
         'notify_url':'http://{}{}'.format(host,reverse('paypal-ipn')),
         'return_url':'http://{}{}'.format(host,reverse('paypal_compeleted_view')),
         'cancel_url':'http://{}{}'.format(host,reverse('paypal_failed_view'))
     }
    paypal__payment_button = PayPalPaymentsForm(initial=paypal_dict)
    cart_total_amount=0
    if 'cart_data_obj'in request.session:

        host=request.get_host()
        cart_total_amount=0
        total_price= 0
        transaction_id=datetime.datetime.now().timestamp()
        print(transaction_id)
        #create customer
        customer,created = Customer.objects.get_or_create(user=request.user,name=request.user.username,email=request.user.email)
        #create order
        order=Order.objects.create(
            customer=customer,
            transaction_id=str(transaction_id)   
        )
        if 'cart_data_obj'in request.session:

            for p_id, item in request.session['cart_data_obj'].items():
                total_price += int(item['quantity'])*float(item['price'])
                total_price = round(total_price, 2)  
                cart_total_amount += int(item['quantity'])*float(item['price'])
                cart_total_amount = round(cart_total_amount, 2)        
            #create cart order item       
                product=Product.objects.get(id=p_id)
                OrderItem.objects.create(
                    product=product,
                    order=order,
                    quantity=request.session['cart_data_obj'][p_id]['quantity'],
                    total=total_price
                )           
        paypal_dict={
            'business':settings.PAYPAL_RECEIVER_EMAIL,
            'amount':cart_total_amount,
            'item_name':'Order-Item-NO-'+str(order.transaction_id),
            'currency_code':'USD',
            'notify_url':'http://{}{}'.format(host,reverse('paypal-ipn')),
            'return_url':'http://{}{}'.format(host,reverse('paypal_compeleted_view')),
            'cancel_url':'http://{}{}'.format(host,reverse('paypal_failed_view'))
        }
        paypal__payment_button = PayPalPaymentsForm(initial=paypal_dict)
        active_address = ShippingAddress.objects.filter(customer=customer,status=True).all().first()
        total_count=WishList.objects.filter(customer=customer).count()            
        return render(request,'new cart/checkout.html',{'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount,'paypal__payment_button':paypal__payment_button,'active_address':active_address,'total_count':total_count})

@csrf_exempt
def ecpay_view(request):
    return HttpResponse(main()) 




def paypal_compeleted_view(request):
    cart_total_amount=0

def paypal_compeleted_view(request):   
    cart_total_amount=0
    cart_data=request.session['cart_data_obj']

    if 'cart_data_obj'in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['quantity'])*float(item['price'])
            cart_total_amount = round(cart_total_amount, 2)
        
        return render(request,'new cart/payapl-completed.html',{'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount })
    del request.session['cart_data_obj']
    
    return render(request,'new cart/payapl-completed.html',{'cart_data':cart_data,'totalcartitems':len(cart_data),'cart_total_amount':cart_total_amount })



def paypal_failed_view(request):
    return render(request,'new cart/paypal-failed.html')



# def pdf_generate(request):
#     username=request.user.username
        
#     html_content =request.GET['pdf_content']
#     print(html_content)
#     options = {
#         'encoding': 'UTF-8',
#         'no-outline': None,
        
#     }
#     pdf = pdfkit.from_string(html_content, False,configuration=pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'),options=options)
#     print(pdf)
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="{username}.pdf"'
#     response.write(pdf)

#     return response

def order_detail(request,o_id):
    order=Order.objects.get(id=o_id)
    orderitem= OrderItem.objects.filter(order=order).all()
    context={
        'orderitem':orderitem
    }

    return  render(request,'new cart/order_detail.html',context)


def make_address_default(request):
    id=request.GET['id']
    print(id)
    ShippingAddress.objects.update(status=False)
    ShippingAddress.objects.filter(id=id).update(status=True)
    return JsonResponse({'boolean':True})

def wishlist_view(request):
    wishlist= WishList.objects.all()
    context={
        'ws':wishlist
    }
    return render(request,'new cart/wishlist.html',context)

def add_to_wishlist(request):
    pid=request.GET['id']
    product=Product.objects.get(id=pid)
    customer=Customer.objects.get(user=request.user)
    wishlist_count=WishList.objects.filter(customer=customer,product=product).count()
    
    if wishlist_count > 0:
        context={
            'boolean':True
        }
    else:
        new_wishlist=WishList.objects.create(customer=customer,product=product)
    total_count=WishList.objects.filter(customer=customer).count()
    print(total_count)
    context={
        'boolean':True,
        'wishlist_count':wishlist_count,
        'total_count':total_count
    }
      
    return JsonResponse(context)

def delete_from_wishlist(request):
    customer=Customer.objects.get(user=request.user)
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    WishList.objects.get(customer=customer,product=product).delete()
    
    new_wishlist=WishList.objects.filter(customer=customer).order_by('-date')
    amount=WishList.objects.filter(customer=customer).count()
    print(new_wishlist)
    data=render_to_string('new cart/async/wish-list.html',{'ws':new_wishlist})
    return JsonResponse({'data':data,'amount':amount})