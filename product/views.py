from django.shortcuts import render, get_object_or_404
from .models import Item, Order, OrderItem, BillingAddress, Payment, ContactMessage
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm, ContactForm,CustomerInfoForm
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import get_template, render_to_string
# Create your views here.





    
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
          
            'order' : order
        }
        return render(self.request, 'checkout-page.html',context)
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                street_address = form.cleaned_data.get('street_address')
                phone = form.cleaned_data.get('phone')
                # country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                payment_option = form.cleaned_data.get('payment_option')  
                # save_info = form.cleaned_data.get('save_info')
               
                billing_address = BillingAddress(
                    user = self.request.user,
                    name = name,
                    street_address = street_address,
                    phone = phone,
                    zip=zip,
                    # country=country
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                if payment_option == 'P':
                    return redirect('product:pay-paystack')
                # elif payment_option == 'PY':
                    #     return redirect('product:payment', payment_option='payu')
                else:
                    messages.warning(self.request, "Failed Checkout")
                    return redirect('product:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("product:shop")


class PaystackView(View):
  
    def get(self, *args, **kwargs):
        customer_form = CustomerInfoForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        # order_item = OrderItem.objects.get(user=self.request.user, ordered=False)
        name = order.billing_address.name
        amount = order.get_total()
        user = self.request.user
        email = self.request.user.email
        if order.billing_address:
            context ={
            'order': order,
            'customer_form': customer_form,
            'amount':amount,
            'email':email,
            'name': name,
          
           
            }
            #if 
         ## create payment 

            payment = Payment()
            # payment.user = self.request.user
            # payment.amount = amount
            # # payment.timestap 
            # payment.save()
            # template = render_to_string('email_template.html', context)
    
            # # ##assign payment to the order

            # order.ordered = True
            # order.payment = payment
            # order.save()
            # email = EmailMessage(
            #     'Thank You For Choosing Us',
            #     template,
            #     settings.EMAIL_HOST_USER,
            #     [email]

                

            # )
            # email.send()
            return render(self.request, 'paystack.html', context)
        else:
            messages.warning(self.request, "You have not added billing address")
            return redirect("product:checkout")
    

       


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
            return redirect("product:shop")


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
        contact = ContactMessage(
            name = name,
            email = email,
            phone= phone,
            subject= subject,
            message= message
            )
        contact.save()
        send_mail(
        'New Contact Form From Nakedsolar Contact Form',
        context,
        email,
        ['themajorresources@gmail.com']
        )
        
        return redirect('/success/')
           
    return render(request, 'contact.html', context)


# def customer_info(request):
#     customer_form = CustomerInfoForm()
#     order = Order.objects.get(user=request.user, ordered=False)
#     amount = order.get_total() 
#     email = request.user.email
    
#     form = {
#             'order':order,
#             'customer_form': customer_form,
#            'amount':amount,
#             'email':email
#         }
   
#     # ## create payment 
#     # payment = Payment()
#     # payment.charge_id = 
#     # payment.user = request.user
#     # payment.amount = amount
#     # payment.save()
    
#     # ##assign payment to the order

#     # order.ordered = True
#     # order.payment = payment
#     # order.save()
#     return render(request, 'customer_info.html', 
#                     form)

def customer_info(request):
    if request.method == 'POST':
        customer_form = CustomerInfoForm(request.method)
        if customer_form.is_valid()and customer_form.cleaned_data:
            customer_form.save()
            email ={
                'email':customer_form.email
            }
            return render(request, 'payment.html', email
                          )
        else:
            return HttpResponse('Invalid input try again!!!')
    else:
        customer_form = CustomerInfoForm()
        order = Order.objects.get(user=request.user, ordered=False)
        amount = order.get_total() 
        email = request.user.email
       
        form ={
            'customer_form': customer_form,
            'amount':amount,
            'email': email
        }
        return render(request, 'customer_info.html', form)