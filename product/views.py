from django.shortcuts import render, get_object_or_404
from .models import Item, Order, OrderItem, BillingAddress, Coupon, Payment, ContactMessage
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm,CouponForm, ContactForm
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template
# Create your views here.



def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')
    
class HomeView(ListView):
    model = Item
    ##pagination on shop online page
    paginate_by = 20
    template_name = "home-page.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-page.html'


class CheckoutView(View):
    def get(self,  *args, **kwargs):
        #form
        order = Order.objects.get(user=self.request.user, ordered=False)
        
        form = CheckoutForm
        context = {
            'form' :form,
            'couponform': CouponForm(),
             'order' : order
        }
        return render(self.request, 'checkout-page.html',context)
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None )
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                payment_option = form.cleaned_data.get('save_info')
                #TODO
                # save_info = form.cleaned_data.get('save_info')
               
                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_address,
                    zip=zip,
                    country=country
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                
                if payment_option == 'P':
                    return redirect('product:payment', payment_option='paystack')
                elif payment_option == 'PY':
                    return redirect('product:payment', payment_option='payu')
                else:
                    messages.warning(self.request, "Failed Checkout")
                    return redirect('product:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("product:order")

class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
            'order' : order 
            }
            return render(self.request, 'payment.html', context)
        else:
            messages.warning(self.request, "You have not added billing address")
            return redirect("product:checkout")
    
    def post(self,*args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        amount = order.get_total()

        order.ordered = True
     

       


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self,  *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order exisits
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect('product:products', slug=slug)
        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
            return redirect('product:products', slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
    return redirect('product:products', slug=slug)

@login_required
def add_single_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order exisits
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect('product:order')
        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
            return redirect('product:order')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
    return redirect('product:order')


@login_required
def add_home_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order exisits
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect('product:shop')
        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
            return redirect('product:shop')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
    return redirect('product:shop')


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('product:products', slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect('product:products', slug=slug)
    return redirect('product:products', slug=slug)


@login_required
def remove_Single_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
            else:
                order.items.remove(order_item)
            order_item.save()
            messages.info(request, "This item quantity was updated ")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('product:order')
    else:
        messages.info(request, "You do not have an active order")
        return redirect('product:order')
    return redirect('product:order')


@login_required
def remove_order_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('product:products')
    else:
        messages.info(request, "You do not have an active order")
        return redirect('product:order')
    return redirect('product:order')


def contact(request):
    form = ContactForm(request.POST)
    context = {
        'form':form
        }
    if form.is_valid():
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone')
        subject = form.cleaned_data.get('suject')
        message = form.cleaned_data.get('message')
        template = get_template('contact.txt')
        content = {
            'name': name,
            "email": email,
            "phone": phone,
            'subject': subject,
            'message': message

        }
        context = template.render(content)
        send_mail(
        'New Contact Form From Nakedsolar Contact Form',
        context,
        email,
        ['themajorresources@gmail.com']
        )
        
        return redirect('/success/')
           
    return render(request, 'contact.html', context)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon doesn't exist")
        return redirect('product:checkout')

        

class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "You have successfully added coupon")
                return redirect('product:checkout')
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect('product:checkout')


        