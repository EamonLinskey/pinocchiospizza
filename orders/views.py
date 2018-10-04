from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.core import serializers
from django.shortcuts import render
from django.urls import reverse 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import PriceList, SizeList, Style, Food, Extra
from decimal import *
import re
import json
import stripe

stripe.api_key = "sk_test_cYmMASmzfTiT23KKKMz6iRDt"

foodContext = {
    	"foods": Food.objects.all(),
    	"extras": Extra.objects.all()
    }

OrdersToFill = []
OrdersFilled = []
TAX = Decimal(0.0625)
orderCount = 0

class Item:
	def __init__(self, food, style, size, toppings, numToppings, quantity):
		self.food = food
		self.style = style	
		self.size = size
		self.toppings = toppings
		self.numToppings = numToppings
		self.quantity = quantity
		self.key = food+style+size+''.join(toppings)+numToppings
	def addQuantity(i):
		self.quantity += i
	def toList(self):
		return [self.food, self.style, self.size, self.toppings, self.numToppings, self.quantity] 


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
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("orders"))
		else:
			return render(request, "orders/signIn.html", {"message": "Invalid Credentials"})
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
		email = request.POST["email"]
		username = request.POST["username"]
		confirmPassword = request.POST["confirmPassword"]
		password = request.POST["password"]
		

		if (len(User.objects.filter(username=username)) > 0):
			return render(request, "orders/register.html", {"message": "That username is taken"})
		if (len(User.objects.filter(email=email))>0):
			return render(request, "orders/register.html", {"message": "That email is taken"})
		if (email == "" or username == "" or password == "" or confirmPassword == ""):
			return render(request, "orders/register.html", {"message": "Fields cannot be blank"})
		if (not re.match(r"[^@]+@[^@]+\.[^@]+", email)):
			return render(request, "orders/register.html", {"message": "You must input valid email"})
		if (confirmPassword != password):
			return render(request, "orders/register.html", {"message": "Passwords did not match"})
		else:
			try: 
				user = User.objects.create_user(username=username, email=email, password=password)
			except:
				return render(request, "orders/register.html", {"message": "An unknown error occured"})
			login(request, user)
			return HttpResponseRedirect(reverse("orders"))
	else:
		return HttpResponseRedirect(reverse("orders"))

def menu(request):
	return render(request, "orders/menu.html", foodContext)

def style(request, food):
	context={
		"foods": Food.objects.all().filter(name=food.title())
	}
	if request.user.is_authenticated:
		return render(request, "orders/styles.html", context)
	else:
		return HttpResponseRedirect(reverse("signIn"))

def getPrice(food, style, size, numTop):
	food = food.replace("%20", " ")
	print("A")
	print(food)
	if Food.objects.all().filter(name__iexact=food):
		print("B")
		selectedFood = Food.objects.all().filter(name__iexact=food)[0]
		if selectedFood:
			print("C")
			selectedStyle = selectedFood.style.all().filter(name__iexact=style)[0]
			if selectedStyle:
				print("D")
				selectedSizeList = getattr(selectedStyle.sizeList, size.lower())
				if selectedSizeList:
					print("E")
					selectedPrice = getattr(selectedSizeList, numTop)
					if selectedPrice:
						print("F")
						return selectedPrice 


	return None

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


# def sendOrder(request):
# 	global orderCount

# 	if not request.is_ajax() or not request.method=='POST':
# 		return HttpResponseRedirect(reverse("index"))
# 	else:
# 		info = []
# 		order = json.loads(request.POST["order"])
# 		for item in request.POST:
# 			if item != "order":
# 				info.append(request.POST[item])
# 		OrdersToFill.append([order, info, orderCount])
# 		orderCount += 1
# 		#OrdersToFill.append(order)
# 		return HttpResponse(200)

def unfilledOrders (request):
	if request.user.is_staff:
		context = {	"orders": OrdersToFill,
						"filled": False		
						}
		return render(request, "orders/staffOrders.html", context)
	else:
		return HttpResponseRedirect(reverse("index"))

def filledOrders (request):
	if request.user.is_staff:
		context = {	"orders": OrdersFilled,
					"filled": True		
					}
		return render(request, "orders/staffOrders.html", context)
	else:
		return HttpResponseRedirect(reverse("index"))

def completedOrder (request):
	if request.is_ajax() and request.method=='POST':
		global OrdersToFill
		print("---------")
		print(type(request.POST["orderId"]))
		print(OrdersToFill[0][3])
		print(request.POST["orderId"])
		

		for i in range(len(OrdersToFill)):
			if str(OrdersToFill[i][3]) == request.POST["orderId"]:
				print("yeah")
				OrdersFilled.append(OrdersToFill[i])
				del OrdersToFill[i]
				print(OrdersToFill)
				return HttpResponse(200)

		return HttpResponse(501)
	elif request.user.is_staff:
		filledOrders = {"orders": OrdersFilled}
		return render(request, "orders/completeOrders.html", filledOrders)
	else:
		return HttpResponseRedirect(reverse("index"))

def success (request):
	if request.user.is_authenticated:
		return render(request, "orders/sucess.html")
	else:
		return HttpResponseRedirect(reverse("signIn"))

def isValidItem(item):
	if isinstance(item, (list,)) and len(item) == 6:
		print("passed 1")
		if isinstance(item[0], (str,)) and isinstance(item[1], (str,)) and isinstance(item[2], (str,)) and isinstance(item[4], (str,)):
			print("passed 2")
			print(item[5])
			print(item[3])
			print(type(item[5]))
			print(type(item[3]))
			if isinstance(item[5], (int,)) and isinstance(item[3], (list,)):
				print("passed 3")
				item[1] = item[1].replace("%20", " ")
				if getPrice(item[1], item[2], item[0], item[4]) != None:
					print("passed 4")
					print(item[1])
					print(Food.objects.all().filter(name__iexact=item[1]))
					legalToppings = Food.objects.all().filter(name__iexact=item[1])[0]
					legalToppings = legalToppings.style.all().filter(name__iexact=item[2])[0].legalExtras.all()
					for topping in item[3]:
						print("passed 5")
						if not legalToppings.filter(name__iexact=topping):
							print("failed 6")
							return False
					return True
	return False

def isValidOrder(order):
	if isinstance(order, (list,)):
		for item in order:
			if not(isValidItem(item)):
				print(item)
				print("first False")
				return False
		print("first true")
		return True
	else:
		print(type(order))
		print(type(["1", "2", "3"]))
		print("last false")
		return False

def calculatePrice(order):
	price = Decimal(0.00)
	for item in order:
		print(item)
		itemPrice = getPrice(item[1], item[2], item[0], item[4])
		if itemPrice:

			price = price + round((itemPrice* item[5]), 2)
	return price

def chargeStripe(token, price):
	priceInCents = int(price*100)
	charge = stripe.Charge.create(
    	amount=priceInCents,
    	currency='usd',
    	description='Pinoccios Pizza',
    	source=token,
		)
	return 

def charge(request):
	global orderCount
	global OrdersToFill
	deliveryInfo = ['address', 'apt-num', 'city', 'zip-code', 'del-inst', 'phone', 'payment']
	requiredInfo = ['address', 'city', 'zip-code', 'phone', 'payment']

	if request.user.is_authenticated and request.method == 'POST':
		# Checks for valid form inputs
		for field in deliveryInfo:
			if field not in request.POST:
				message = {"message": "There was an error with your delivery information"}
				return render(request, "orders/cart.html", message)
		for field in requiredInfo:
			if request.POST[field] == "":
				message = {"message": "Your address, city, zipcode, phone number and payment type is required"}
				return render(request, "orders/cart.html", message)

		# Checks to make sure order was legal
		order = json.loads(request.POST["hidden-order"])
		print("the order is:")
		print(order)
		if not isValidOrder(order):
			message = {'message': "Your order was not valid"}
			return render(request, "orders/cart.html", message)

		# Checks for valid stripe token when card is selected
		if request.POST["payment"] == "card" and 'stripeToken' not in request.POST:
			message = {"message": "You must type your card information or pay with cash"}
			return render(request, "orders/cart.html", message)

		# Checks for a valid price
		price = round(calculatePrice(order) * (Decimal('1.0') + TAX), 2)
		if price <= 0:
			message = {"message": "Your order was not valid"}
			return render(request, "orders/cart.html", message)

		#Appends appropriate info to the order
		info = []
		for item in request.POST:
			if item in deliveryInfo:
				info.append(request.POST[item])
		OrdersToFill.append([order, info, price, orderCount])
		orderCount += 1

		if 'stripeToken' in request.POST and request.POST["payment"] == "card":
			token = request.POST['stripeToken']
			chargeStripe(token, price)

		return render(request, "orders/sucess.html")
	else:
		return HttpResponseRedirect(reverse("index"))
