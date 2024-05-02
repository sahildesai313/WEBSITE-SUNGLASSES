from django.contrib import admin
from django.urls import path
from .views import (
    LoginView,
    RegisterView,
    HomeView,
    AddtocartView,
    ProfileView,
    EditProfileView,
    ChangepasswordView,
    LogoutView,
    ForgotView,
    OtpView,
    ResetpasswordView,
    AboutView,
    ContactView,
    GlassView,
    ShopView,
    AddressdetailsView,
    PaymentView,
    ConfirmationorderView,
    CartView,
    # RemoveFromCartView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("home/", HomeView.as_view(), name="home"),
    path("home/product/<int:image_id>/", AddtocartView.as_view(), name="product"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("edit/", EditProfileView.as_view(), name="edit"),
    path("profile/change/", ChangepasswordView.as_view(), name="change"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("forgot/", ForgotView.as_view(), name="forgot"),
    path("otp/", OtpView.as_view(), name="otppage"),
    path("reset/", ResetpasswordView.as_view(), name="reset"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("glass/", GlassView.as_view(), name="glass"),
    path("shop/", ShopView.as_view(), name="shop"),
    path("address/", AddressdetailsView.as_view(), name="Address"),
    path("payment/", PaymentView.as_view(), name="payment"),
    path("confirm/", ConfirmationorderView.as_view(), name="confirm"),
    path("cart/", CartView.as_view(), name="cart"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
