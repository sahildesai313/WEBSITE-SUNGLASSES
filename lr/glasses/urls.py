from django.contrib import admin
from django.urls import path
from .views import (
    LoginView,
    RegisterView,
    HomeView,
    ProductView,
    ProfileView,
    EditView,
    ChangeView,
    LogoutView,
    ForgotView,
    OtpView,
    ResetView,
    AboutView,
    ContactView,
    GlassView,
    ShopView,
    AddressdetailsView,
    PaymentView,
    ConfirmationView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("home/", HomeView.as_view(), name="home"),
    path("home/product/<int:image_id>/", ProductView.as_view(), name="product"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("edit/", EditView.as_view(), name="edit"),
    path("profile/change/", ChangeView.as_view(), name="change"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("forgot/", ForgotView.as_view(), name="forgot"),
    path("otp/", OtpView.as_view(), name="otppage"),
    path("reset/", ResetView.as_view(), name="reset"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("glass/", GlassView.as_view(), name="glass"),
    path("shop/", ShopView.as_view(), name="shop"),
    path("address/", AddressdetailsView.as_view(), name="Address"),
    path("payment/", PaymentView.as_view(), name="payment"),
    path("confirm/", ConfirmationView.as_view(), name="confirm"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
