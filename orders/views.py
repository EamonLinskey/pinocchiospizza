from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.core import serializers
from django.shortcuts import render
from django.urls import reverse 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import PriceList, SizeList, Style, Food, Extra
import re
import json

foodContext = {
    	"foods": Food.objects.all(),
    	"extras": Extra.objects.all()
    }

OrdersToFill = []
OrdersFilled = []
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

def prices(request, food, style, size, numTop):
	if request.user.is_authenticated:
		selectedFood = Food.objects.all().filter(name__iexact=food)[0]
		selectedStyle = selectedFood.style.all().filter(name__iexact=style)[0]
		selectedSizeList = getattr(selectedStyle.sizeList, size.lower())
		selectedPrice = getattr(selectedSizeList, numTop)

		return HttpResponse(selectedPrice, content_type='application/json')
	else:
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


def sendOrder(request):
	global orderCount

	if not request.is_ajax() or not request.method=='POST':
		return HttpResponseRedirect(reverse("index"))
	else:
		info = []
		order = json.loads(request.POST["order"])
		for item in request.POST:
			if item != "order":
				info.append(request.POST[item])
		OrdersToFill.append([order, info, orderCount])
		orderCount += 1
		#OrdersToFill.append(order)
		return HttpResponse(200)

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
		print("---------")
		print(type(request.POST["orderId"]))
		global OrdersToFill

		for i in range(len(OrdersToFill)):
			if str(OrdersToFill[i][2]) == request.POST["orderId"]:
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
