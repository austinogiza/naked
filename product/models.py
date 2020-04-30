from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField


# Create your models here.

CATEGORY_CHOICE = (
    ('B', 'Batteries'),
    ('IV', 'Inverter'),
    ('SP', 'Solar Panel'),
)

LABEL_CHOICE = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)


class Item(models.Model):
    title = models.CharField(max_length=50, unique=True, blank=False)
    image = models.ImageField(upload_to='photo/', blank=False)
    price = models.FloatField()
    discount = models.CharField(max_length=50, blank=False)
    description = models.TextField(max_length=2550, blank=False)
    specification = models.TextField(max_length=2550, blank=False)

    category = models.CharField(choices=CATEGORY_CHOICE, max_length=2, blank=False)
    label = models.CharField(choices=LABEL_CHOICE, max_length=1, blank=False)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product:products', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('product:add-to-cart', kwargs={'slug': self.slug})
    
    def get_home_to_cart_url(self):
        return reverse('product:add-home-to-cart', kwargs={'slug': self.slug})
        

    def get_remove_from_cart_url(self):
        return reverse('product:remove-from-cart', kwargs={'slug': self.slug})


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_price(self):
        return self.quantity * self.item.discount

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_price()

    def get_final_price(self):
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=False, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=False, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=False, null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        total -= self.coupon.amount
        return total



class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address =  models.CharField(max_length=200)
    zip = models.CharField(max_length=100)
    country = CountryField(multiple=False)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

class Payment(models.Model):
    charge_id = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestap = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class ContactMessage(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=2000)

    def __str__(self):
        return self.name
    
    
    