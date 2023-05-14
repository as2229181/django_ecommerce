from django.urls import path,include
from . import views
from django.contrib import admin






urlpatterns=[
    path("",views.store,name="store"),
    path("cart/",views.cart, name="cart"),
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
    path('test6',views.test6,name='test6'),
    path('test7/<vid>/',views.test7,name='test7'),
    path('test8/<slug:tag_slug>/',views.test8,name='test8'),
    path('ajax_add_review/<sui>',views.ajax_add_review,name='ajax_add_review'),
    path('search',views.search_view,name='search'),
    path('filter_product/',views.filter_product,name='filter_product'),
    ]

