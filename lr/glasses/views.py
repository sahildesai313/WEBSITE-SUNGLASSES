from django.shortcuts import render
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.response import Response
from .serializers import personSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from .models import person
from django.contrib import messages
import random
from django.core.mail import EmailMessage

# Create your views here.



class RegisterView(generics.CreateAPIView):
    serializer_class = personSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "register.html"

    def get(self, request):
        serializer = personSerializer()
        return render(request, self.template_name, {"serializer": serializer})

    def post(self, request):
        username = request.data.get("username")
        if person.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get("phone")
            password = serializer.validated_data.get("password")
            confirm_password = serializer.validated_data.get("confirmpassword")

            if len(phone) != 10 :
                messages.error(request,"phone number is not Valid")

            if len(phone) != 10:
                messages.error(request, "phone number is not Valid")

                return redirect("register")

            if password != confirm_password:
                messages.error(request, "Passwords do not match")
                return redirect("register")
            serializer.save()
            return redirect("login")
        return render(request, self.template_name, {"serializer": serializer})
