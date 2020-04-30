from django.contrib import admin

from .models import Order, Item, OrderItem, BillingAddress, Coupon, ContactMessage

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']


admin.site.register(Item)

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BillingAddress)
admin.site.register(Coupon)
admin.site.register(ContactMessage)
