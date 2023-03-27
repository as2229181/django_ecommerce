from django.urls import path,include
from . import views
from django.contrib import admin





urlpatterns=[
    path("",views.store,name="store"),
    path("cart",views.cart, name="cart"),
    path('checkout',views.checkout, name="checkout")
]

