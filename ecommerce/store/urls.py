from django.urls import path,include
from . import views
from django.contrib import admin






urlpatterns=[
    path("",views.store,name="store"),
    path("cart/",views.cart, name="cart1"),
    path('checkout/',views.checkout, name="checkout"),
    path("update_item/",views.updateItem,name="update_item"),
    path("process_order/",views.processOrder,name="processOrder"),
    path('register/',views.register,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('test/',views.test,name='test'),
    path('test1/',views.test1,name='test1'),
    path('test2/',views.test2,name='test2'),
    path('test3/<sui>',views.test3,name='test3'),
    path('test4/',views.test4,name='test4'),
    path('test5/<cid>/',views.test5,name='test5'),
    path('cutsomer_view',views.cutsomer_view,name='cutsomer_view'),
    path('cutsomer_dashboard/<vid>/',views.cutsomer_dashboard,name='cutsomer_dashboard'),
    path('test8/<slug:tag_slug>/',views.test8,name='test8'),
    path('ajax_add_review/<sui>',views.ajax_add_review,name='ajax_add_review'),
    path('search',views.search_view,name='search'),
    path('filter_product/',views.filter_product,name='filter_product'),
    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
    path('cart_view/',views.cart_view,name='cart'),
    path('delete_from_cart/',views.delete_from_cart,name='delete_from_cart'),
    path('update_cart/',views.update_cart,name='update_cart'),
    path('change_cart_quantity/',views.change_cart_quantity,name='change_cart_quantity'),
    path('checkout_view/',views.checkout_view,name='checkout_view'),
    path('ecpay_view/',views.ecpay_view,name='ecpay'),

    #paypal
    path('paypal/',include('paypal.standard.ipn.urls')),
    
    # paypal complete 
    path('paypal_compeleted_view/',views.paypal_compeleted_view,name='paypal_compeleted_view'),
    # paypal failed
    path('paypal_failed_view/',views.paypal_failed_view,name='paypal_failed_view'),

    ]

