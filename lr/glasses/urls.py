from django.contrib import admin
from django.urls import path
from .views import RegisterView, LoginView, HomeView, ForgotView, OtpView, ResetView, ContactView,ShopView,GlassView,AboutView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("", LoginView.as_view(), name="login"),
    path("home/", HomeView.as_view(), name="home"),
    path("forgot/", ForgotView.as_view(), name="forgot"),
    path("otp/", OtpView.as_view(), name="otppage"),
    path("reset/", ResetView.as_view(), name="reset"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("glass/", GlassView.as_view(), name="glass"),
    path("shop/", ShopView.as_view(), name="shop"),

]
