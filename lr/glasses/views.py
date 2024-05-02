from django.shortcuts import render, redirect
from django.contrib import messages
from django.http.request import HttpRequest
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404

from rest_framework.permissions import AllowAny
from rest_framework import generics, serializers, status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import (
    PersonSerializer,
    Forgetserializer,
    Addressserializer,
    Loginserializer,
    ResetpasswordSerializer,
    OtpSerializer,
    ChangeSerializer,
    EditProfileSerializer,
    PaymentSerializer,
    ContactSerializer,
    ProductSerializer,
)
from rest_framework.renderers import TemplateHTMLRenderer

import random
from .models import Person, Product, Address, Card, Cart
from typing import Union


class RegisterView(generics.CreateAPIView):
    serializer_class = PersonSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "register.html"

    def get(self, request: Union[Request, HttpRequest]) -> Union[render, redirect]:
        if "username" in request.session:
            return redirect("home")
        serializer = PersonSerializer()
        return render(request, self.template_name, {"serializer": serializer})

    def post(self, request: Union[Request, HttpRequest]) -> Union[redirect, render]:
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("login")
        messages.error(request, serializer.errors["non_field_errors"][0])
        return render(request, self.template_name)


class LoginView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Loginserializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "login.html"

    def get(self, request: Union[Request, HttpRequest]) -> Union[render, redirect]:
        if "username" in request.session:
            return redirect("home")
        return render(request, self.template_name)

    def post(self, request: Union[Request, HttpRequest]) -> Union[render, redirect]:
        serializer = Loginserializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get("username")
            request.session["username"] = username
            return redirect("home")
        messages.error(request, serializer.errors["non_field_errors"][0])
        return render(request, self.template_name)


class ForgotView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    tempalte_name = "forgot.html"

    def get(self, request: Union[Request, HttpRequest]) -> Union[render, redirect]:
        if "username" in request.session:
            return redirect("home")
        return render(request, self.tempalte_name)

    def post(self, request: Union[Request, HttpRequest]) -> redirect:
        serializer = Forgetserializer(data=request.data)
        if not serializer.is_valid():
            messages.error(request, serializer.errors["non_field_errors"][0])
            return redirect("forgot")
        email = serializer.data["email"]
        otp = str(random.randint(1000, 9999))
        request.session["email"] = email
        request.session["otp"] = otp
        email = EmailMessage(body=otp, to=[email])
        email.send()
        return redirect("otppage")


class OtpView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "otp.html"
    serializer_class = OtpSerializer

    def get(self, request: Union[Request, HttpRequest]) -> Union[render, redirect]:
        if "usernameCreateAPIView" in request.session:
            return redirect("home")
        return render(request, self.template_name)

    def post(self, request: Union[Request, HttpRequest]) -> redirect:
        otp = request.session.get("otp")
        serializer = OtpSerializer(data=request.data, context={"otp": otp})
        if not serializer.is_valid():
            messages.error(request, serializer.errors["non_field_errors"][0])
            return redirect("otppage")
        return redirect("reset")


class ResetpasswordView(GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "resetpassword.html"
    serializer_class = ResetpasswordSerializer

    def get(self, request: Union[Request, HttpRequest]) -> Union[render, redirect]:
        if "username" in request.session:
            return redirect("home")
        return render(request, self.template_name)

    def post(self, request: Union[Request, HttpRequest]) -> redirect:
        email = request.session.get("email")
        serializer = ResetpasswordSerializer(data=request.data, context={"email_id": email})
        if not serializer.is_valid():
            messages.error(request, serializer.errors["non_field_errors"][0])
            return redirect("reset")
        return redirect("login")


class HomeView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "home.html"

    def get(self, request: Union[Request, HttpRequest]) -> Union[render, redirect]:
        if "username" not in request.session:
            return redirect("login")
        Product_details = Product.objects.all()
        return render(
            request, self.template_name, context={"Product_details": Product_details}
        )


class ProfileView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profile.html"

    def get(self, request: Union[Request, HttpRequest]) -> render:
        if "username" not in request.session:
            return redirect("login")
        username = request.session.get("username")
        Person_details = Person.objects.filter(username=username)
        return render(request, self.template_name, context={"details": Person_details})


class EditProfileView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "editprofile.html"
    serializer_class = EditProfileSerializer

    def get(self, request: Union[Request, HttpRequest]) -> Union[render, redirect]:
        if "username" not in request.session:
            return redirect("login")
        username = request.session.get("username")
        person_details = Person.objects.filter(username=username)
        return render(
            request, self.template_name, context={"person_details": person_details}
        )

    def post(self, request: Union[Request, HttpRequest]) -> redirect:
        username = request.session.get("username")
        serializer = EditProfileSerializer(
            data=request.data, context={"user_id": username}
        )
        if serializer.is_valid():
            return redirect("profile")
        messages.error(request, serializer.errors["non_field_errors"][0])
        return redirect("edit")


class ChangepasswordView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "changepassword.html"
    serializers = ChangeSerializer

    def get(self, request: Union[Request, HttpRequest]) -> Union[render, redirect]:
        if "username" not in request.session:
            return redirect("login")
        return render(request, self.template_name)

    def post(self, request: Union[Request, HttpRequest]) -> redirect:
        username = request.session.get("username")
        serializer = ChangeSerializer(data=request.data, context={"user_id": username})
        if serializer.is_valid():
            return redirect("profile")
        messages.error(request, serializer.errors["non_field_errors"][0])
        return redirect("change")


class GlassView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "glass.html"

    def get(self, request: Union[Request, HttpRequest]) -> Union[render, redirect]:
        if "username" not in request.session:
            return redirect("login")
        return render(request, self.template_name)

    def post(self, request: Union[Request, HttpRequest]) -> render:
        product_details = Product.objects.all()
        return render(
            request, self.template_name, context={"product_details": product_details}
        )


class AboutView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "about.html"

    def get(self, request: Union[Request, HttpRequest]) -> Union[render, redirect]:
        if "username" not in request.session:
            return redirect("login")
        return render(request, self.template_name)


class ContactView(generics.CreateAPIView):
    serializer_class = ContactSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "contact.html"

    def get(self, request: Union[Request, HttpRequest]) -> Union[render, redirect]:
        if "username" not in request.session:
            return redirect("login")
        serializer = ContactSerializer()
        return render(request, self.template_name,  {"serializer": serializer})

    def post(self, request: Union[Request, HttpRequest]) -> Union[redirect, render]:
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("home")
        return render(request, self.template_name)


class AddressdetailsView(generics.CreateAPIView):
    serializer_class = Addressserializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "address.html"

    def get(self, request: Union[Request, HttpRequest]) -> render:
        if "username" not in request.session:
            return redirect("login")
        return render(request, self.template_name)

    def post(self, request: Union[Request, HttpRequest]) -> Union[render, redirect]:
        username = request.session.get("username")
        serializer = Addressserializer(
            data=request.data, context={"username": username}
        )
        if serializer.is_valid():
            serializer.save()
            return redirect("cart")
        return redirect("Address")


class ConfirmationorderView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "confirmation.html"

    def get(self, request: Union[Request, HttpRequest]) -> render:
        if "username" not in request.session:
            return redirect("home")

        person = Person.objects.get(username=request.session["username"])
        cart_items = Cart.objects.filter(person=person)
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        return render(
            request,
            self.template_name,
            {"cart_items": cart_items, "total_price": total_price},
        )

    def post(self, request: Union[Request, HttpRequest]) -> redirect:
        return redirect("shop")


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request: Union[Request, HttpRequest]) -> redirect:
        del request.session["username"]
        return redirect("login")


class ShopView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "shop.html"

    def get(self, request: Union[Request, HttpRequest]) -> Union[render, redirect]:
        if "username" not in request.session:
            return redirect("login")
        male_product = Product.objects.filter(gender=1)
        female_product = Product.objects.filter(gender=2)
        all_product = Product.objects.all()

        return render(
            request,
            self.template_name,
            context={
                "male_product": male_product,
                "female_product": female_product,
                "all_product": all_product,
            },
        )



# class ProductView(generics.CreateAPIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = "product.html"
#     serializer_class = ProductSerializer

#     def get(self, request: Union[Request, HttpRequest], image_id) -> render:
#         if "username" not in request.session:
#             return redirect("login")
#         product_details = Product.objects.filter(id=image_id)
#         product_id = product_details.values("id").first()
#         get_id = product_id.get("id")
#         request.session["id"] = get_id
#         return render(
#             request, self.template_name, context={"product_details": product_details}
#         )  


class AddtocartView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "cart.html"

    def get(self, request: Union[Request, HttpRequest], image_id) -> redirect:
        if "username" not in request.session:
            return redirect("login")
        product = Product.objects.get(id=image_id)
        person = Person.objects.get(username=request.session["username"])
        quantity = request.POST.get("quantity", 1)
        cart_item, created = Cart.objects.get_or_create(person=person, product=product)
        cart_item.quantity += int(quantity)
        cart_item.save()
        return redirect("cart")


class CartView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "cart.html"

    def get(self, request: Union[Request, HttpRequest]) -> redirect:
        if "username" not in request.session:
            return redirect("login")

        person = Person.objects.get(username=request.session["username"])
        cart_items = Cart.objects.filter(person=person)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        amount = sum(item.quantity * item.product.price for item in cart_items)
        total_price += 10

        return render(
            request,
            self.template_name,
            {"cart_items": cart_items, "total_price": total_price, "amount": amount},
        )

    def post(self, request):
        if "username" not in request.session:
            return redirect("login")

        person = Person.objects.get(username=request.session["username"])

        if "checkout" in request.POST:
            if Cart.objects.filter(person=person).exists():
                return redirect("payment")
            else:
                return redirect("cart")

        if "product_id" in request.POST:
            product_id = request.POST.get("product_id")
            product = Product.objects.get(id=product_id)
            cart_item = Cart.objects.get(person=person, product=product)
            cart_item.delete()
            return redirect("cart")


class PaymentView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "payment.html"
    serializer_class = PaymentSerializer

    def get(self, request: Union[Request, HttpRequest]) -> Union[render, redirect]:
        if "username" not in request.session:
            return redirect("login")
        id = request.session.get("id")
        product_details = Product.objects.filter(id=id)
        person = Person.objects.get(username=request.session["username"])
        cart_items = Cart.objects.filter(person=person)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        amount = 0
        for p in cart_items:
            value = p.quantity * p.product.price
            amount = amount + value
        total_price = amount + 10

        return render(
            request,
            self.template_name,
            {"cart_items": cart_items, "total_price": total_price, "amount": amount},
        )

    def post(self, request):
        username = request.session.get("username")
        serializer = PaymentSerializer(
            data=request.data, context={"username": username}
        )
        if serializer.is_valid():
            serializer.save()
            return redirect("confirm")
        messages.error(request, serializer.errors["non_field_errors"][0])
        return redirect("payment")
