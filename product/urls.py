
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import (HomeView,
 ItemDetailView, 
 add_to_cart, 
 remove_from_cart, 
 OrderSummaryView, 
 remove_Single_from_cart, 
 add_single_to_cart,
  remove_order_from_cart,
  CheckoutView,
 PaymentView,
AddCouponView,
 add_home_to_cart
                    )

app_name = 'product'

urlpatterns = [
     
    path('', views.home, name='home'),
       path('about/', views.about, name='about'),
    path('shop/', HomeView.as_view(), name='shop'),
    path('contact/', views.contact, name='contact'),
    path('products/<slug>/', ItemDetailView.as_view(), name='products'),
    path('order/', OrderSummaryView.as_view(), name='order'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
      path('add-home-to-cart/<slug>/',  add_home_to_cart, name='add-home-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/',
         remove_Single_from_cart, name='remove-single-item-from-cart'),
    path('add-item-to-cart/<slug>/',
         add_single_to_cart, name='add-single-item-to-cart'),
    path('remove-order-from-cart/<slug>/',
         remove_order_from_cart, name='remove-order-from-cart'),
    path('payment/<payment_option>/',
         PaymentView.as_view(), name='payment'),

  

]
