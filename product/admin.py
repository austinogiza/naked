from django.contrib import admin

from .models import Order, Item, OrderItem, BillingAddress,  ContactMessage, Payment

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'ordered')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount')

admin.site.register(Item )
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(BillingAddress)
admin.site.register(ContactMessage)
