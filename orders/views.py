from django.core import serializers
from django.shortcuts import render
from django.urls import reverse 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import (HttpResponse, HttpResponseRedirect, 
						HttpResponseNotAllowed)
from .models import PriceList, SizeList, Style, Food, Extra
from decimal import *
import re
import json
import stripe


# Set global variables
stripe.api_key = "sk_test_cYmMASmzfTiT23KKKMz6iRDt"
foodContext = {
    	"foods": Food.objects.all(),
    	"extras": Extra.objects.all()
}
OrdersToFill = []
OrdersFilled = []
TAX = Decimal(0.0625)
orderCount = 0

# Create your views here.
def index(request):
	return render(request, "orders/index.html")

def signIn(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse("orders"))
	else:
		return render(request, "orders/signIn.html")

def signedIn(request):
	if (request.method == "POST"):
		password, username = "", ""

		if request.POST["password"]:
			password = request.POST["password"]
		if request.POST["username"]:
			username= request.POST["username"]
		try:
			user = authenticate(request, username=username, password=password)
			login(request, user)
			return HttpResponseRedirect(reverse("orders"))
		except:
			return render(request, "orders/signIn.html", 
							{"message": "Invalid Credentials",
							 "username": username})
	else:
		return HttpResponseRedirect(reverse("index"))

def orders(request):
	if request.user.is_authenticated:
		return render(request, "orders/orders.html", foodContext)
	else:
		return HttpResponseRedirect(reverse("signIn"))

def signOut(request):
	if request.user.is_authenticated:
		logout(request)
	return HttpResponseRedirect(reverse("signIn"))

def user_view(request):
    if not request.user.is_authenticated:
    	return HttpResponseRedirect(reverse("register"))
    return HttpResponseRedirect(reverse("orders"), context)

def register(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse("orders"))
	else:
		return render(request, "orders/register.html")

def registered(request):
	if (request.method == "POST"):
		# Set variables from form
		email = request.POST["email"]
		username = request.POST["username"]
		confirmPassword = request.POST["confirmPassword"]
		password = request.POST["password"]
		
		# Validate inputs
		if (email == "" or username == "" or password == "" or 
		confirmPassword == ""):
			return render(request, "orders/register.html", 
						{"message": "Fields cannot be blank",
						"email": email, "username": username})
		if (len(User.objects.filter(username=username)) > 0):
			return render(request, "orders/register.html", 
						{"message": "That username is taken",
						"email": email, "username": username})
		if (len(User.objects.filter(email=email))>0):
			return render(request, "orders/register.html", 
						{"message": "That email is taken",
						"email": email, "username": username})
		if (not re.match(r"[^@]+@[^@]+\.[^@]+", email)):
			return render(request, "orders/register.html", 
						{"message": "You must input valid email",
						"email": email, "username": username})
		if (confirmPassword != password):
			return render(request, "orders/register.html", 
						{"message": "Passwords did not match",
						"email": email, "username": username})
		else:
			try: 
				# Create new user
				user = User.objects.create_user(username=username, email=email, 
												password=password)
				login(request, user)
				return HttpResponseRedirect(reverse("orders"))
			except:
				return render(request, "orders/register.html", 
							{"message": "An unknown error occured",
							"email": email, "username": username})	
	else:
		return HttpResponseRedirect(reverse("orders"))

def menu(request):
	return render(request, "orders/menu.html", foodContext)

def style(request, food):
	context={ "foods": Food.objects.all().filter(name=food.title()) }
	if request.user.is_authenticated:
		return render(request, "orders/styles.html", context)
	else:
		return HttpResponseRedirect(reverse("signIn"))

def getPrice(food, style, size, numTop):
	# Clean food value
	food = food.replace("%20", " ")
	try:
		# Attempt to get the price of particular item
		Food.objects.all().filter(name__iexact=food)
		selectedFood = Food.objects.all().filter(name__iexact=food)[0]
		selectedStyle = selectedFood.style.all().filter(name__iexact=style)[0]
		selectedSizeList = getattr(selectedStyle.sizeList, size.lower())
		selectedPrice = getattr(selectedSizeList, numTop)
		return selectedPrice 
	except:
		return None

# An API like page that lists the price of specific foods based on url
def prices(request, food, style, size, numTop):
	if request.user.is_authenticated:
		selectedPrice = getPrice(food, style, size, numTop)
		if selectedPrice:
			return HttpResponse(selectedPrice, content_type='application/json')
	return HttpResponseRedirect(reverse("signIn"))

def cart(request):
	if request.user.is_authenticated:
		return render(request, "orders/cart.html")
	else:
		return HttpResponseRedirect(reverse("signIn"))

def checkout(request):
	if request.user.is_authenticated:
		return render(request, "orders/checkout.html")
	else:
		return HttpResponseRedirect(reverse("signIn"))

def unfilledOrders (request):
	if request.user.is_staff:
		context = {	"orderInfo": OrdersToFill,
					"filled": False		
				}
		return render(request, "orders/staffOrders.html", context)
	else:
		return HttpResponseRedirect(reverse("index"))

def filledOrders (request):
	if request.user.is_staff:
		context = {	"orderInfo": OrdersFilled,
					"filled": True		
				}
		return render(request, "orders/staffOrders.html", context)
	else:
		return HttpResponseRedirect(reverse("index"))

def completedOrder (request):
	if request.is_ajax() and request.method=='POST':
		# clearify global variables
		global OrdersToFill

		# Find the order with the mathing id number and move it to filled list
		for i in range(len(OrdersToFill)):
			if (str(OrdersToFill[i]["orderCount"]) == 
			str(request.POST["orderId"])):
				OrdersFilled.append(OrdersToFill[i])
				del OrdersToFill[i]
				return HttpResponse(200)
		return HttpResponse(501)
	else:
		return HttpResponseRedirect(reverse("index"))


def isValidItem(item):
	# Checks type and length to make sure appropriate
	if isinstance(item, (dict,)) and len(item) == 6:
		# Checks eto make sure each category is an sppropriate type
		if (isinstance(item["size"], (str,)) and 
		isinstance(item["food"], (str,)) and isinstance(item["style"], (str,)) 
		and isinstance(item["numToppings"], (str,))):
			if (isinstance(item["quantity"], (int,)) 
			and isinstance(item["toppings"], (list,))):

				# Cleans food variable
				item["food"] = item["food"].replace("%20", " ")
				try:
					# Sees if valid price exists for item
					getPrice(item["food"], item["style"], item["size"], 
							item["numToppings"])
					
					# Checks individual topping to make sure each is legal
					food = Food.objects.all().get(name__iexact=item["food"])
					legalToppings = food.style.all().get(
						name__iexact=item["style"]).legalExtras.all()
					for topping in item["toppings"]:
						if not legalToppings.filter(name__iexact=topping):
							return False
					return True
				except:
					return False
	return False

def isValidOrder(order):
	# checks that order is of a valid type then validates each item 
	if isinstance(order, (list,)):
		for item in order:
			if not(isValidItem(item)):
				return False
		return True
	else:
		return False

def calculatePrice(order):
	# Initialize price
	price = Decimal(0.00)

	# Iterate price for each item
	for item in order:
		itemPrice = getPrice(item["food"], item["style"], item["size"], 
							item["numToppings"])
		if itemPrice:
			price = price + round((itemPrice* item["quantity"]), 2)
	return price

# Stripe charge according to their documentation
def chargeStripe(token, price):
	priceInCents = int(price*100)
	charge = stripe.Charge.create(
    	amount=priceInCents,
    	currency='usd',
    	description='Pinoccios Pizza',
    	source=token)
	return 

def charge(request):
	# Clearify global variables
	global orderCount
	global OrdersToFill

	deliveryInfo = ['address', 'apt-num', 'city', 'zip-code', 'del-inst', 
					'phone', 'payment']
	requiredInfo = ['address', 'city', 'zip-code', 'phone', 'payment']

	if request.user.is_authenticated and request.method == 'POST':
		# Checks for valid form inputs
		for field in deliveryInfo:
			if field not in request.POST:
				message = {"message": 
					"There was an error with your delivery information"}
				return render(request, "orders/cart.html", message)
		for field in requiredInfo:
			if request.POST[field] == "":
				message = {"message": 
				"Your address, city, zipcode, phone number and payment " \
				"type is required"}
				return render(request, "orders/cart.html", message)

		# Checks to make sure order was legal
		try:
			order = json.loads(request.POST["hidden-order"])
		except:
			message = {'message': "Your order was empty"}
			return render(request, "orders/cart.html", message)

		if not isValidOrder(order):
			message = {'message': "Your order was not valid"}
			return render(request, "orders/cart.html", message)

		# Checks for valid stripe token when card is selected
		if (request.POST["payment"] == "card" and 
		'stripeToken' not in request.POST):

			message = {"message": 
			"You must type your card information or pay with cash"}
			return render(request, "orders/cart.html", message)

		# Checks for a valid price
		price = round(calculatePrice(order) * (Decimal('1.0') + TAX), 2)
		if price <= 0:
			message = {"message": "Your order was not valid"}
			return render(request, "orders/cart.html", message)

		#Appends appropriate info to the order
		info = {"address": request.POST['address'],
				"aptNum": request.POST['apt-num'],
				"zipCode": request.POST['zip-code'],
				"city": request.POST['city'],
				"phone": request.POST['phone'],
				"payment": request.POST['payment'],
				"delInst": request.POST['del-inst']
				}
		
		OrdersToFill.append({"order":order, "info":info, "price":price, 
							"orderCount":orderCount})
		# Iterate order count so that each order can have an id
		orderCount += 1

		# Charges stripe if user used a card
		if 'stripeToken' in request.POST and request.POST["payment"] == "card":
			token = request.POST['stripeToken']
			chargeStripe(token, price)

		return render(request, "orders/sucess.html")
	else:
		return HttpResponseRedirect(reverse("index"))
