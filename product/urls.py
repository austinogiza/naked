
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
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
  paysuccess,
  callback,
  battery,
  solar,
  inverter,
PaystackView,
# checkout,
 add_home_to_cart
                    )

app_name = 'product'

urlpatterns = [
    path('shop/', HomeView.as_view(), name='shop'),
    path('contact/', views.contact, name='contact'),
    path('products/<slug>/', ItemDetailView.as_view(), name='products'),
    path('order/', OrderSummaryView.as_view(), name='order'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
      path('add-home-to-cart/<slug>/',  add_home_to_cart, name='add-home-to-cart'),

    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/',
         remove_Single_from_cart, name='remove-single-item-from-cart'),
    path('add-item-to-cart/<slug>/',
         add_single_to_cart, name='add-single-item-to-cart'),
    path('remove-order-from-cart/<slug>/',
         remove_order_from_cart, name='remove-order-from-cart'),
     path('customer_info/', views.customer_info,
         name='customer_info'),
     path('pay-paystack/',
       PaystackView.as_view(), name='pay-paystack'),
     path('paystack-success/', views.paysuccess, name='paystack-success'),
     path('callback/', views.callback, name='callback'),
     path('solar/', views.solar, name='solar'),
     path('inverter/', views.inverter, name='inverter'),
     path('battery/',views.battery, name='battery'),
 
]
