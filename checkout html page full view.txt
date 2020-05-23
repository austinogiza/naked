from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
import pypaystack
from pypaystack import Transaction
from django.conf import settings
from order.models import Order, OrderItem
from shop.models import CustomUser
from django.template.loader import get_template
from django.core.mail import EmailMessage
from shop.forms import CustomUserCreationForm
import sys

'''Check if there's a session ID on user browser'''
def _cart_id(request):
	"""
	Create a session tied to the logged in user.
	Look for an existing cart tied to the user.
	If no user is there, create one tied to te current session with the session key.
	(Expand later to allow unauthenticated users to use the cart)
	"""

	request.session['user'] = "visitor" #expand later to allow users not is_authenticated


	#keep each user's session tied to their username to retrieve their cart
	if request.user.is_authenticated:
		request.session['user'] = request.user.username
		cart = request.session['user']
	else:
		cart = request.session.session_key
		if not cart:
			cart = request.session.create()
	return cart

'''Add product to shopping cart'''
def add_cart(request, product_id):
	"""
	Get POST information and extract the size selected. If there is no cart, create one.
	Check if item exists in cart, if not create one, if it does, increment it by one.
	"""
	if request.method == "POST":
		size = request.POST["size"]
	product = Product.objects.get(id=product_id)
	try:
		cart = Cart.objects.get(cart_id=_cart_id(request))
	except Cart.DoesNotExist:
		cart = Cart.objects.create(
			cart_id=_cart_id(request)
			)
		cart.save()
	try:
		#size = CartItem.objects.get(notes=notes)
		cart_item = CartItem.objects.get(product=product, cart=cart, notes=size)
		if cart_item.quantity < cart_item.product.stock:
			cart_item.quantity  += 1
		cart_item.save()
	except CartItem.DoesNotExist:
		cart_item = CartItem.objects.create(
			product=product,
			quantity = 1,
			notes = size,
			cart = cart
			)
		cart_item.save()
	return redirect('cart:cart_detail')

'''Show items/details in the shopping cart'''
def cart_detail(request, total=0, counter=0, cart_items = None):
	"""
	Get the cart and its contents and calculate the total. Initialize PAystack auth details
	Grab the logged in user's details.
	From the POST queryset from Paystack, get required details and use it to create the order and the items
	associated with it. Send an email with the order details to the user's email.
	Create
	"""
	try:
		cart = Cart.objects.get(cart_id=_cart_id(request))
		cart_items = CartItem.objects.filter(cart=cart, active=True)
		for cart_item in cart_items:
			total += (cart_item.product.price * cart_item.quantity)
			counter += cart_item.quantity
	except ObjectDoesNotExist:
		pass

	return render(request, 'cart.html', dict(cart_items = cart_items, total = total, counter = counter))


def cart_remove(request, product_id):
	"""
	Fetch the cart and if the item is more than one, decrement it by one otherwise delete it.
	"""
	cart = Cart.objects.get(cart_id=_cart_id(request))
	product = get_object_or_404(Product, id=product_id)
	cart_item = CartItem.objects.get(product=product, cart=cart)
	if cart_item.quantity > 1:
		cart_item.quantity -= 1
		cart_item.save()
	else:
		cart_item.delete()
	return redirect('cart:cart_detail')

def full_remove(request, product_id, ):
	"""
	Remove all instances of the product from the cart including variations
	"""
	cart = Cart.objects.get(cart_id=_cart_id(request))
	product = get_object_or_404(Product, id=product_id)
	cart_item = CartItem.objects.filter(product=product, cart=cart) #filterting removes all instances and variations fix later to remove only the variation
	cart_item.delete()
	return redirect('cart:cart_detail')

def shipping(request, total=0, counter=0, cart_items = None, shipping_option = None, shipping_method = None, shipping_cost = 0):
	metro_en = ['coal camp community bank', 'holy ghost cathedral (inside)', 'ekulu primary school (trans)', 'park lane (g.r.a.)', 'shoprite (g.r.a.)', 'christ the king parish (g.r.a.)', "st mary's trans ekulu (trans)", 'damija bus stop (trans)', 'dental (trans)', 'st theresa (abakpa)', 'zoo estate (g.r.a.)', 'st mulumba (new hall)', 'bisala road (ind. layout)', 'blessed sacrament parish (ind. layout)', 'spar (new layout)', 'toscana (ind. layout)', 'elli court (ind. layout)', 'the base (ind. layout)', 'holy trinity (ind. layout)', 'st paul (awkunanaw)', 'unec (new layout)', 'one day bus stop (awkunanaw)', 'st gregory (idaw river)', 'bigard memorial seminary (uwnai)', 'vincentians (maryland)']

	pickup = ["showroom", "workshop"]
	other_15 = ["Lagos", "Abuja", "Port Harcourt", "Bayelsa", "Calabar", "Jos", "Lagos - Aja", "Lagos - Orile","Lagos - Mazamaza", "Lagos - Demorose", "Lagos - Ikorodu", "Lagos - Ejigbo",
"Lagos - Ajegunle", "Lagos - Sango Ota", "Lagos - Oshodi", "Lagos - Ojuelegba", "Abuja - Utako", "Abuja - Zuba", "Abuja - Gwagwalada", "Abuja - Kubwa",
"Abuja - Kuje", "Abuja - Bwari", "Abuja - Maraba"]
	other_12 = ["Umuahi", "Owerri", "Onitsha"]
	other_1000 = ["Ebonyi"]
	other_600 = ["Nsukka"]
	others = other_15 + other_12 + other_1000 + other_600
	others.sort()
	other = [item.lower() for item in others]
	try:
		cart = Cart.objects.get(cart_id=_cart_id(request))
		cart_items = CartItem.objects.filter(cart=cart, active=True)
		items = [item.quantity for item in cart_items]
		noOfItems =sum(items)
		for cart_item in cart_items:
			total += (cart_item.product.price * cart_item.quantity)
			counter += cart_item.quantity
	except ObjectDoesNotExist:
		pass

	if request.method == 'POST':
		try:
			shipping_method = request.POST["ship_method"]
			shipping_option = request.POST["ship_method"]
			if shipping_method in pickup:
				shipping_method = "pickup (No Charges)"
				shipping_cost = 0

				#Save details as part of cart
				cart.shipping_cost = str(shipping_cost) #our db value for shipping_cost is a string
				cart.shipping_method = shipping_method
				cart.shipping_option = shipping_option #choice of method
				cart.save()
			elif shipping_method in metro_en:
				shipping_method = "Enugu Metro"
				shipping_cost = 100 #Flat 100 bucks for now

				#Save details as part of cart
				cart.shipping_cost = str(shipping_cost) #our db value for shipping_cost is a string
				cart.shipping_method = shipping_method
				cart.shipping_option = shipping_option #choice of method
				cart.save()
			elif shipping_method in other:
				#Find the right cost of shipping by destination group
				#All delivery to a group is same for up to 2 else charged delivery + 50% of delivery cost
				if shipping_method in [ line.lower() for line in other_1000]:
					if noOfItems <= 2:
						shipping_cost = 1000
					else:
						shipping_cost = 1500
				elif shipping_method in [ line.lower() for line in other_12]:
					if noOfItems <= 2:
						shipping_cost = 1200
					else:
						shipping_cost = noOfItems * 1800
				elif shipping_method in [ line.lower() for line in other_15]:
					if noOfItems <= 2:
						shipping_cost = 1500
					else:
						shipping_cost = 2250
				elif shipping_method in [ line.lower() for line in other_600]:
					if noOfItems <= 2:
						shipping_cost = 600
					else:
						shipping_cost = 900

				shipping_method = "Other"
				#Save details as part of cart
				cart.shipping_cost = str(shipping_cost) #our db value for shipping_cost is a string
				cart.shipping_method = shipping_method
				cart.shipping_option = shipping_option #choice of method
				cart.save()
		except:
			pass
	else:
		print("Eagle landed on Shipping, awaiting shipping POST of shipping options.")
	return render (request, 'shipping.html', dict(
		cart_items = cart_items,
		total = total,
		shipping_method = shipping_method,
		shipping_cost=shipping_cost,
		shipping_option = shipping_option,
		grand_total = shipping_cost + total, #shipping_cost is still an int. we only added to db as str
		metro_en = metro_en,
		other = other,
		pickup = pickup))

def checkout(request, total=0, counter=0, cart_items = None, shipping_cost = 0, shipping_method=None):
	try:
		cart = Cart.objects.get(cart_id=_cart_id(request))
		cart_items = CartItem.objects.filter(cart=cart, active=True)
		noOfItems = [item.quantity for item in cart_items]
		for cart_item in cart_items:
			total += (cart_item.product.price * cart_item.quantity)
			counter += cart_item.quantity
		shipping_cost = cart.shipping_cost #a string value, remember
		shipping_method = cart.shipping_method
		shipping_option = cart.shipping_option
	except ObjectDoesNotExist:
		pass
	##Trying to grab detaisl for myself from the User module
	# if request.user.is_authenticated:
	# 	emailAddress= str(request.user.email)
	pypaystack.api_key = settings.PAYSTACK_SECRET_KEY
	paystack_total = int((total + int(shipping_cost)) * 100) #shipping cost was str, take to int here
	#description = 'e-Duu Designz Online Store - New Order'
	data_key = settings.PAYSTACK_PUBLISHABLE_KEY

	if request.user.is_authenticated:
		try:
			email= str(request.user.email)
			full_name = str(request.user.get_full_name())
			address = str(request.user.address)
			city = str(request.user.city)
			phone = str(request.user.phone)
		except:
			print("User is not authenticated or has no email on record.")

	if request.method == 'POST':
		token = request.POST['reference']
		try:
			transactions=pypaystack.Transaction(authorization_key=pypaystack.api_key)
			verification = transactions.verify(request.POST['reference'])
			fname = verification[3]['metadata']['custom_fields'][0].get('first_name')
			lname = verification[3]['metadata']['custom_fields'][1].get('last_name')
			address = verification[3]['metadata']['custom_fields'][2].get('address')
			city = verification[3]['metadata']['custom_fields'][3].get('city')
			phone = verification[3]['metadata']['custom_fields'][4].get('phone')
		except:
			print("We could not fetch pypaystack details")
		#Creating an order
		try:
			order_details = Order.objects.create(
				token = token,
				product_total = total,
				shipping_cost = int(shipping_cost),#This is a string from db, we need it as an int here
				total = total + int(shipping_cost), #shipping cost was str, take to int here
				shipping_method = shipping_method,
				shipping_option = shipping_option,
				email = email,
				billingName = full_name,
				billingAddress = address,
				billingCity = city,
				billingPhoneNo = phone
				)
			order_details.save()
			for order_item in cart_items:
				oi = OrderItem.objects.create(
					product = order_item.product.name,
					quantity = order_item.quantity,
					price = order_item.product.price,
					size = order_item.notes,
					order = order_details
					)
				oi.save()
				#reduce product stock#
				products = Product.objects.get(id=order_item.product.id) #get the product by id for each as we dey for loop still
				products.stock = int(order_item.product.stock - order_item.quantity) #reduce the stock by order quantity
				products.save() #save what remains of the product
				#get the variation object via product name (a foreignkey of Products) and the size (a str obj)
				#This should match a signle variation item, deduct it and save the remainder
				try:
					size = Variation.objects.get(product=products, title=order_item.notes)
					size.v_stock -= order_item.quantity
					size.save()
				except:
					e = sys.exc_info()
					print(e)
					print("We couldn't deduct size/variation inventory")						
				
				order_item.delete() #delete the item from the cart
			try:
				#Trying to send email using the email function
				sendEmail(order_details.id)
				print("Order Email Sent to customer")
			except IOError as e:
				return e
				print("Order email was not sent")
				print(e)
			return redirect('order:thanks', order_details.id)
		except ObjectDoesNotExist:
			pass

	return render(request, 'checkout.html', dict(cart_items = cart_items,
		product_total = total,
		counter = counter,
		data_key=data_key,
		paystack_total=paystack_total,
		emailAddress=email,
		phone=phone,
		address=address,
		shipping_cost = shipping_cost,
		shipping_method = shipping_method,
		shipping_option = shipping_option,
		grand_total= int(shipping_cost)+total,
		city=city))

def pay_on_delivery(request, total=0, counter=0, pod=False):
	try:
		cart = Cart.objects.get(cart_id=_cart_id(request))
		cart_items = CartItem.objects.filter(cart=cart, active=True)
		noOfItems = [item.quantity for item in cart_items]
		for cart_item in cart_items:
			total += (cart_item.product.price * cart_item.quantity)
			counter += cart_item.quantity
		shipping_cost = cart.shipping_cost #a string value, remember
		shipping_method = cart.shipping_method
		shipping_option = cart.shipping_option
	except ObjectDoesNotExist:
		pass
	
	if request.user.is_authenticated:
		try:
			email= str(request.user.email)
			full_name = str(request.user.get_full_name())
			address = str(request.user.address)
			city = str(request.user.city)
			phone = str(request.user.phone)
		except:
			print("User is not authenticated or has no email on record.")

	if request.POST:
		try:
			order_details = Order.objects.create(
				product_total = total,
				shipping_cost = int(shipping_cost),#This is a string from db, we need it as an int here
				total = total + int(shipping_cost), #shipping cost was str, take to int here
				shipping_method = shipping_method,
				shipping_option = shipping_option,
				email = email,
				billingName = full_name,
				billingAddress = address,
				billingCity = city,
				billingPhoneNo = phone,
				pod = True
				)
			order_details.save()
			for order_item in cart_items:
				oi = OrderItem.objects.create(
					product = order_item.product.name,
					quantity = order_item.quantity,
					price = order_item.product.price,
					size = order_item.notes,
					order = order_details
					)
				oi.save()
				#reduce product stock#
				products = Product.objects.get(id=order_item.product.id) #get the product by id for each as we dey for loop still
				products.stock = int(order_item.product.stock - order_item.quantity) #reduce the stock by order quantity
				products.save() #save what remains of the product
				#get the variation object via product name (a foreignkey of Products) and the size (a str obj)
				#This should match a signle variation item, deduct it and save the remainder
				try:
					size = Variation.objects.get(product=products, title=order_item.notes)
					size.v_stock -= order_item.quantity
					size.save()
				except:
					e = sys.exc_info()
					print(e)
					print("We couldn't deduct size/variation inventory")						
				
				order_item.delete() #delete the item from the cart
			try:
				#Trying to send email using the email function
				sendEmail(order_details.id)
				print("Order Email Sent to customer")
			except IOError as e:
				return e
				print("Order email was not sent")
				print(e)
			return redirect('order:thanks', order_details.id)
		except ObjectDoesNotExist:
			pass
	return render(request, 'pay_on_delivery.html', dict(cart_items = cart_items,
		product_total = total,
		emailAddress=email,
		phone=phone,
		address=address,
		full_name = full_name,
		shipping_cost = shipping_cost,
		shipping_method = shipping_method,
		shipping_option = shipping_option,
		grand_total= int(shipping_cost)+total,
		city=city,
		pod = pod))

def sendEmail(order_id):
	"""
	Send email to logged in user with their order details
	"""
	transaction = Order.objects.get(id=order_id)
	order_items = OrderItem.objects.filter(order=transaction)
	grand_total = transaction.total
	try:
		subject = "e-Duu Designz Store - New Order #{}".format(transaction.id)
		to = ['{}'.format(transaction.email)]
		from_email = "orders@eduudesignzstore.com"
		order_information = {
		'transaction' : transaction,
		'order_items' : order_items,
		'grand_total' : grand_total
		}
		message = get_template('email/email.html').render(order_information)
		msg = EmailMessage(subject, message, to=to, from_email=from_email, bcc=['eduudesignz@gmail.com'])
		msg.content_subtype = 'html'
		msg.send()
	except IOError as e:
		return e