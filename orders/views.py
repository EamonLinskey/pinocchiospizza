from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import ToppingList, Price, Style, Pizza, Topping, Pasta, Salad, DinnerPlatter, Sub, Extra
import re

foodContext = {
    	"pizzas": Pizza.objects.all(),
    	"subs": Sub.objects.all(),
    	"toppings": Topping.objects.all(),
    	"pastas": Pasta.objects.all(),
    	"salads": Salad.objects.all(),
    	"dinnerPlatters": DinnerPlatter.objects.all(),
    	"menu": [Pizza.objects.all(), Sub.objects.all(), Pasta.objects.all(), Salad.objects.all(),  DinnerPlatter.objects.all()]
    }


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



