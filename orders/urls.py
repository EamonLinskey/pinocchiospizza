
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("menu", views.menu, name="menu"),
    path("signIn", views.signIn, name="signIn"),
    path("signedIn", views.signedIn, name="signedIn"),
    path("signOut", views.signOut, name="signOut"),
    path("register", views.register, name="register"),
    path("registered", views.registered, name="registered"),
    path("orders", views.orders, name="orders"),
    path("orders/<str:food>", views.style, name="style"),
    path("prices/<str:food>/<str:style>/<str:size>/<str:numTop>", 
            views.prices, name="prices"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("unfilledOrders", views.unfilledOrders, name="unfilledOrders"),
    path("completedOrder", views.completedOrder, name="completedOrder"),
    path("filledOrders", views.filledOrders, name="filledOrders"),
    path("charge", views.charge, name="charge")
]
