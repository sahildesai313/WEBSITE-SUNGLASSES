from django.shortcuts import render, redirect
from django.contrib import messages
from django.http.request import HttpRequest
from django.core.mail import EmailMessage



from rest_framework.permissions import AllowAny
from rest_framework import generics, serializers
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import PersonSerializer, Forgetserializer, Addressserializer, Loginserializer, ResetSerializer, OtpSerializer, ChangeSerializer, EditProfileSerializer, PaymentSerializer
from rest_framework.renderers import TemplateHTMLRenderer

import random
from .models import Person, Product, Address, Card
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
        messages.error(request, serializer.errors['non_field_errors'][0])
        return render(request, self.template_name)
    

class LoginView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Loginserializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "login.html"

    def get(self, request: Union[Request, HttpRequest])  -> Union[render, redirect]:
        if "username" in request.session:
              return redirect("home")
        return render(request, self.template_name)

    def post(self, request: Union[Request, HttpRequest])  -> Union[render, redirect]:
        serializer = Loginserializer(data=request.data) 
        if serializer.is_valid():
            username = serializer.data.get('username')
            request.session['username'] = username
            return redirect("home")
        messages.error(request, serializer.errors['non_field_errors'][0])
        return render(request, self.template_name)
    
      

class ForgotView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    tempalte_name = "forgot.html"

    def get(self, request: Union[Request, HttpRequest])  -> Union[render, redirect]:
        if "username" in request.session:
            return redirect("home")
        return render(request, self.tempalte_name)

    def post(self, request: Union[Request, HttpRequest])  ->  redirect:
        serializer = Forgetserializer(data = request.data)
        if not serializer.is_valid():
            messages.error(request, serializer.errors['non_field_errors'][0])
            return redirect("forgot")
        email =serializer.data['email']
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

    def get(self, request: Union[Request, HttpRequest])  -> Union[render, redirect]:
        if "usernameCreateAPIView" in request.session:
            return redirect("home")
        return render(request, self.template_name)

    def post(self, request: Union[Request, HttpRequest])  ->  redirect:
        otp = request.session.get("otp")
        serializer = OtpSerializer(data = request.data,context={'otp': otp})
        if not serializer.is_valid():
            messages.error(request, serializer.errors['non_field_errors'][0])
            return redirect("otppage")
        return redirect("reset")


class ResetView(GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "reset.html"
    serializer_class = ResetSerializer  

    def get(self, request: Union[Request, HttpRequest])  -> Union[render, redirect]:
        if "username" in request.session:
            return redirect("home")
        return render(request, self.template_name)

    def post(self, request:  Union[Request, HttpRequest])  ->  redirect:
        email= request.session.get('email')
        serializer = ResetSerializer(data = request.data, context={'email_id': email})
        if not serializer.is_valid():
            messages.error(request, serializer.errors['non_field_errors'][0])
            return redirect('reset')
        return redirect("login")
        
            
class HomeView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "home.html"

    def get(self, request:  Union[Request, HttpRequest]) -> Union[render, redirect] :
        if "username" not in request.session:
            return redirect("login")
        Product_details = Product.objects.all()
        return render(request, self.template_name, context={"Product_details": Product_details})


class ProfileView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profile.html"

    def get(self, request:  Union[Request, HttpRequest])  -> render:
        if "username" not in request.session:
            return redirect("login")
        username = request.session.get("username")
        Person_details = Person.objects.filter(username=username)        
        return render(request, self.template_name, context={"details": Person_details})


class ProductView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "product.html"

    def get(self, request:  Union[Request, HttpRequest], image_id)  -> render:
        Product_details = Product.objects.filter(id=image_id)
        return render(request, self.template_name, context={"Product_details": Product_details})


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request:  Union[Request, HttpRequest])  ->  redirect:
        del request.session["username"]
        return redirect("login")


class ChangeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "changepassword.html"
    serializers = ChangeSerializer

    def get(self, request:  Union[Request, HttpRequest])  -> Union[render, redirect]:
        if "username" not in request.session:
            return redirect("login")
        return render(request, self.template_name)

    def post(self, request:  Union[Request, HttpRequest])  -> redirect:
        username = request.session.get("username")
        serializer = ChangeSerializer(data=request.data, context={'user_id': username})
        if serializer.is_valid():
            return redirect("profile")     
        messages.error(request, serializer.errors['non_field_errors'][0])
        return redirect('change')


class EditView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "edit.html"
    serializer_class = EditProfileSerializer

    def get(self, request:  Union[Request, HttpRequest])  -> Union[render, redirect]:
        if "username" not in request.session:
            return redirect("login")
        username = request.session.get("username")
        person_details = Person.objects.filter(username=username)
        return render(request, self.template_name,context={'person_details':person_details})    

    def post(self, request:  Union[Request, HttpRequest])  ->  redirect:
        username = request.session.get("username")
        serializer = EditProfileSerializer(data= request.data, context={'user_id':username})
        if serializer.is_valid():
            return redirect("profile")
        messages.error(request, serializer.errors['non_field_errors'][0])
        return redirect('edit')



class AboutView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "about.html"

    def get(self, request:  Union[Request, HttpRequest])  -> Union[render, redirect]:
        if "username" not in request.session:   
            return redirect("login")
        return render(request, self.template_name)


class ContactView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "Contact.html"

    def get(self, request:  Union[Request, HttpRequest])  -> Union[render, redirect]:
        if "username" not in request.session:
            return redirect("login")
        return render(request, self.template_name)


class ShopView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "shop.html"

    def get(self, request:  Union[Request, HttpRequest])  -> Union[render, redirect]:
        if "username" not in request.session:
            return redirect("login")
        product_details = Product.objects.all()
        return render(request, self.template_name,context={"product_details": product_details})


class GlassView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "glass.html"

    def get(self, request:  Union[Request, HttpRequest])  -> Union[render, redirect]:
        if "username" not in request.session:
            return redirect("login")
        return render(request, self.template_name)

    def post(self, request:  Union[Request, HttpRequest])  -> render:
        product_details = Product.objects.all()
        return render(request, self.template_name, context={"product_details": product_details})


class AddressdetailsView(generics.CreateAPIView):
    serializer_class = Addressserializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "address.html"

    def get(self, request:  Union[Request, HttpRequest])  -> render:
        if "username" not in request.session:
            return redirect("login")
        return render(request, self.template_name)
    
    def post(self, request:  Union[Request, HttpRequest]) -> Union[render, redirect]:
        username  = request.session.get('username')
        serializer = Addressserializer(data = request.data, context = {'username': username})
        if serializer.is_valid():
            pincode =serializer.data.get('pincode')
            request.session['pincode'] = pincode
            serializer.save()
            return redirect('payment')
        return redirect('Address')


class PaymentView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "payment.html"
    serializer_class = PaymentSerializer

    def get(self, request:  Union[Request, HttpRequest])  -> Union[render, redirect]:
        if "username" not in request.session:
            return redirect("login")
        return render(request, self.template_name)
    
    def post(self,request:  Union[Request, HttpRequest])  ->  redirect:
        pincode = request.session.get('pincode')
        serializer = PaymentSerializer(data = request.data, context = {'pincode': pincode})
        print("serializer------->",serializer)
        if serializer.is_valid():
            serializer.save()
            return redirect('thank')
        messages.error(request, serializer.errors)
        return redirect('payment')
    

class ThankView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "thanks.html"

    def get(self,request: Union[Request, HttpRequest]) -> render:
        if "username" not in request.session:
            return redirect("login")
        return render(request, self.template_name)
        
        