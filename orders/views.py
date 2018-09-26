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


def updateCart(request):
	if not request.is_ajax() or not request.method=='POST':
		return HttpResponseRedirect(reverse("index"))
	print(request.POST.getlist('toppings[]'))
	newItem = Item(request.POST["food"].replace('%20', ' '), request.POST["style"], request.POST["size"], request.POST.getlist('toppings[]'), request.POST["numToppings"], request.POST["quantity"])
	print(json.dumps(newItem, default=lambda o: o.__dict__))
	isUnique = True
	order = request.session.get('order')
	if (order):
		for item in json.loads(order):
			if item.key == newItem.key:
				item.addQuantity(newItem.quantity)
				isUnique = False
		if isUnique:
			request.session['order'].append([json.dumps(newItem, default=lambda o: o.__dict__)])
	else:
		request.session['order'] = [json.dumps(newItem, default=lambda o: o.__dict__)]
	
	print(json.loads(request.session['order'][0])["food"])
	return HttpResponse(200)
