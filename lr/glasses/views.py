from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import *
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib import messages
import random
from django.core.mail import EmailMessage
from .models import *
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class RegisterView(generics.CreateAPIView):
    serializer_class = personSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "register.html"

    def get(self, request):
        if "username" in request.session:
            return redirect("home")
        serializer = personSerializer()
        return render(request, self.template_name, {"serializer": serializer})

    def post(self, request):
        username = request.data.get("username")
        phone = request.data.get("phone")
        if person.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if len(phone) != 10:
            messages.error(request, "phone number is not Valid")
            return redirect("register")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get("phone")
            password = serializer.validated_data.get("password")
            confirm_password = serializer.validated_data.get("confirmpassword")

            if password != confirm_password:
                messages.error(request, "Passwords do not match")
                return redirect("register")
            serializer.save()
            return redirect("login")
        return render(request, self.template_name, {"serializer": serializer})


class LoginView(generics.CreateAPIView):
    serializer_class = personSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "login.html"

    def get(self, request):
        if "username" in request.session:
            return redirect("home")
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = person.objects.filter(username=username).first()
            if user and user.password == password:
                messages.success(request, "Login successful")
                request.session["username"] = username
                return redirect("home")
            else:
                messages.error(request, "Invalid Username or Password")
                return redirect("login")
        else:

            return render(request, self.template_name)


class ForgotView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    tempalte_name = "forgot.html"

    def get(self, request):
        if "username" in request.session:
            return redirect("home")
        return render(request, self.tempalte_name)

    def post(self, request):
        email = request.POST.get("email")
        print("email:", email)
        try:
            user = person.objects.filter(email=email)
            request.session["email"] = email
            print(user)
        except:
            return redirect("forgot")

        if user:
            otp = str(random.randint(1000, 9999))
            request.session["otp"] = otp
            print("otp :", otp)
            email = EmailMessage(body=otp, to=[email])
            email.send()
            return redirect("otppage")
        else:
            messages.error(request, "Email Not Valid")
            return redirect("forgot")


class OtpView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "otp.html"

    def get(self, request):
        if "username" in request.session:
            return redirect("home")
        return render(request, self.template_name)

    def post(self, request):
        enter_otp = request.POST.get("enter_otp")
        otp = request.session.get("otp")
        if otp != enter_otp:
            messages.error(request, " Invalid OTP")
            return redirect("otppage")
        else:
            return redirect("reset")


class ResetView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "reset.html"

    def get(self, request):
        if "username" in request.session:
            return redirect("home")
        return render(request, self.template_name)

    def post(self, request):
        new_password = request.POST.get("new_password")
        confirmpassword = request.POST.get("confirm__password")
        print("new_password:", new_password)
        print("confirm_password:", confirmpassword)
        email = request.session.get("email")

        if new_password == confirmpassword:
            try:
                user = person.objects.filter(email=email).first()
                user.password = new_password
                user.confirmpassword = confirmpassword
                user.save()
                return redirect("login")
            except person.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            messages.error(request, "password not match")
            return redirect("reset")


class HomeView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "home.html"

    def get(self, request):
        if "username" not in request.session:
            return redirect("login")
        data = product.objects.all()
        print(data)
        return render(request, self.template_name, context={"datas": data})


class ProductView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "product.html"

    def get(self, request, image_id):
        data = product.objects.filter(id=image_id)
        maledata = maleproduct.objects.filter(id=image_id)
        femaledata = femaleproduct.objects.filter(id=image_id)
        return render(
            request,
            self.template_name,
            context={"datas": data, "maledata": maledata, "femaledata": femaledata},
        )


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        del request.session["username"]
        return redirect("login")


class ProfileView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profile.html"

    def get(self, request):
        if "username" not in request.session:
            return redirect("login")
        username = request.session.get("username")
        data = person.objects.filter(username=username)
        return render(request, self.template_name, context={"datas": data})
   

class ChangeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "changepassword.html"

    def get(self, request):
        if "username" not in request.session:
            return redirect("login")
        return render(request, self.template_name)

    def post(self, request):
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirmpassword = request.POST.get("confirm__password")
        print("old:", old_password)
        print("new:", new_password)
        print("con:", confirmpassword)

        try:
            user = person.objects.get(password=old_password)

        except:
            messages.error(request, "old password not correct")
            return redirect("change")

        if new_password == confirmpassword:
            if user:
                user.password = new_password
                user.confirmpassword = confirmpassword
                user.save()
                return redirect("profile")
        else:
            messages.error(request, "password not match")
            return redirect("change")


class EditView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "edit.html"

    def get(self, request):
        if "username" not in request.session:
            return redirect("login")
        username = request.session.get("username")
        user=person.objects.filter(username=username)
        return render(request, self.template_name,context={'user':user})    


    def post(self, request):
        username = request.session.get("username")
        fullname = request.POST.get("fullname")
        phone = request.POST.get("phone")
        country = request.POST.get("country")

        print(fullname, phone, country, username)
        user = person.objects.get(username=username)

        if user:
            user.fullname = fullname
            user.phone = phone
            user.country = country
            user.save()
        return redirect("profile")

    def get(self, request):
        if "username" not in request.session:
            return redirect("login")
        username = request.session.get("username")
        user = person.objects.filter(username=username)
        return render(request, self.template_name, context={"user": user})


class AboutView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "about.html"

    def get(self, request):
        if "username" not in request.session:
            return redirect("login")
        return render(request, self.template_name)


class ContactView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "Contact.html"

    def get(self, request):
        if "username" not in request.session:
            return redirect("login")
        return render(request, self.template_name)


class ShopView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "shop.html"

    def get(self, request):
        if "username" not in request.session:
            return redirect("login")

        data=product.objects.all()
        maledata=maleproduct.objects.all()
        femaledata=femaleproduct.objects.all()
        return render(request, self.template_name,context={'datas':data,'maledata':maledata,'femaledata':femaledata})


class AddressView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "address.html"

    def get(self,request):
        return render(request,self.template_name)


        data = product.objects.all()
        maledata = maleproduct.objects.all()
        femaledata = femaleproduct.objects.all()
        return render(
            request,
            self.template_name,
            context={"datas": data, "maledata": maledata, "femaledata": femaledata},
        )



class GlassView(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "glass.html"

    def get(self, request):
        if "username" not in request.session:
            return redirect("login")
        return render(request, self.template_name)

    def post(self, request):
        data = product.objects.all()
        return render(request, self.template_name, context={"data": data})


class Addressdetails(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "address.html"

    def get(self, request):
        if "username" not in request.session:
            return redirect("login")
        return render(request, self.template_name)
    
    def post(self, request):
        locality = request.POST.get("locality")
        address = request.Post.get("address")
        pincode = request.POST.get("pincode")
        city = request.POST.get("city")
        state = request.POST.get("state")

        
class Payment(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "payment.html"

    def get(self, request):
        if "username" not in request.session:
            return redirect("login")
        return render(request, self.template_name)

