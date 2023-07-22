from django.urls import path,include
from . import views
from django.contrib import admin






urlpatterns=[
    path("",views.store,name="store"),
    # path('checkout/',views.checkout, name="checkout"),
    # path("update_item/",views.updateItem,name="update_item"),
    # path("process_order/",views.processOrder,name="processOrder"),
    path('register/',views.register,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),

    path('contact/',views.contact,name='contact'),
    path('intro/',views.intro,name='intro'),
    path('product/get/<sui>/',views.product,name='product'),

    path('category/get/<cid>/',views.category_view,name='category'),
    path('vendor_view',views.vendor_view,name='vendor_view'),
    path('vender_detail/<vid>/',views.vender_detail,name='vender_detail'),
    path('tag/get/<slug:tag_slug>/',views.tag_view,name='tag'),
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
    #customer dashboard
    path('customer_view/',views.customer_view,name='customer_view'),
    path('customer_detail/<int:c_id>',views.customer_detail,name='customer_detail'),
    #paypal
    path('paypal/',include('paypal.standard.ipn.urls')),

    # paypal complete
    path('paypal_compeleted_view/',views.paypal_compeleted_view,name='paypal_compeleted_view'),
    # paypal failed
    path('paypal_failed_view/',views.paypal_failed_view,name='paypal_failed_view'),

    path('order_detail/<o_id>',views.order_detail,name='order_detail'),
    # pdf generate
    # path('pdf_generate/',views.pdf_generate,name='pdf_generate'),
    path('make_address_default/',views.make_address_default,name='make_address_default'),
    # wishlist
    path('wishlist_view/',views.wishlist_view,name='wishlist_view'),
    # add to wishlist
    path('add_to_wishlist/',views.add_to_wishlist,name='add_to_wishlist'),
    # delete from wishlist
    path('delete_from_wishlist/',views.delete_from_wishlist,name='delete_from_wishlist'),
    # delete from wishlist
    path('contact_us_ajax/',views.contact_us_ajax,name='contact_us_ajax'),
    # delete from wishlist
    path('profile_update/',views.profile_update,name='profile_update'),
    ]

