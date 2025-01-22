from django.contrib import admin
from django.urls import path
from .views import *
from store.middlewares.auth import auth_middleware

urlpatterns = [
    path('', index, name="home_page"),
    path('about', about, name="about_page"),
    path('contact', contact, name="contact_page"),
    path('signup', signup, name="signup_page"),
    path('login', login, name="login_page"),
    path('cart' , auth_middleware(cart), name="cart_page"),
    path('check-out' , checkout, name="checkout_page"),
     path('order' ,  auth_middleware(orderview), name="order_page"),
    path('logout', logout),
]


