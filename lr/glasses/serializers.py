from rest_framework import serializers

from django.core.exceptions import ValidationError

from .models import Person, Address, Card, Contact, Product
import re
from typing import Union


class PersonSerializer(serializers.ModelSerializer):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    gender = serializers.ChoiceField(choices=GENDER_CHOICES)

    class Meta:
        model = Person
        fields = "__all__"

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        confirmpassword = data.get("confirmpassword")
        phone = data.get("phone")

        if Person.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        if len(str(phone)) != 10:
            raise ValidationError("Phone number is not valid")
        if password != confirmpassword:
            raise ValidationError("Passwords do not match")

        return data

    def create(self, validated_data):
        return super().create(validated_data)


class Loginserializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ("username", "password")

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        person_details = Person.objects.filter(
            username=username, password=password
        ).first()
        if not person_details:
            raise ValidationError("Invalid Username or Password")
        return data


class Forgetserializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ("email",)

    def validate(self, data):
        email = data.get("email")
        person_details = Person.objects.filter(email=email)
        if not person_details:
            raise serializers.ValidationError("email address not valid")
        return data


class ResetpasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ("password", "confirmpassword")

    def validate(self, data):
        email = self.context.get("email_id")
        password = data.get("password")
        cpassword = data.get("confirmpassword")

        if password != cpassword:
            raise ValidationError("password not match")

        person_details = Person.objects.get(email=email)
        person_details.password = password
        person_details.save()
        return person_details


class OtpSerializer(serializers.Serializer):
    enter_otp = serializers.CharField()

    def validate(self, data):
        otp = self.context.get("otp")
        enter_otp = data.get("enter_otp")
        if otp != enter_otp:
            raise serializers.ValidationError("Invalid OTP")
        return data


class ChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ("password", "confirmpassword")

    def validate(self, data):
        username = self.context.get("user_id")
        password = data.get("password")
        confirmpassword = data.get("confirmpassword")

        if password != confirmpassword:
            raise ValidationError("password not match")

        person_details = Person.objects.get(username=username)
        person_details.password = password
        person_details.confirmpassword = confirmpassword
        person_details.save()
        data["person_details"] = person_details
        return data


class EditProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = (
            "fullname",
            "phone",
            "country",
        )

    def validate(self, data):
        username = self.context.get("user_id")
        fullname = data.get("fullname")
        phone = data.get("phone")
        country = data.get("country")
        person_details = Person.objects.filter(username=username).first()
        phone_number = re.findall("[a-z]", phone)
        if phone_number:
            raise ValidationError("please enter only number")
        if len(str(phone)) != 10:
            raise ValidationError("Enter 10 digit")
        if person_details:
            person_details.fullname = fullname
            person_details.phone = phone
            person_details.country = country
            person_details.save()
        return data


class Addressserializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ("city", "state", "address", "locality", "pincode")

    def create(self, validated_data):
        username = self.context.get("username")
        person = Person.objects.filter(username=username).first()
        address = Address.objects.get_or_create(person=person, **validated_data)
        return address


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"

    def validate(self, data):
        cardnumber = data.get("cardnumber")
        cvv = data.get("cvv")
        MM= data.get("MM")
        YYYY = data.get("YYYY") 

        if len(cardnumber) != 19:
            raise ValidationError("Enter Valid Carddeatils")
        if len(MM)!= 2 or len(YYYY)!= 4:
            raise ValidationError("Enter valid Carddeatils")
        if len(cvv) != 3:
            raise ValidationError("Enter Valid Carddeatils")
        return data

    def create(self, validated_data):
        username = self.context.get("username")
        person = Person.objects.filter(username=username).first()
        card = Card.objects.get_or_create(person=person, **validated_data)
        return card


class ConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = "__all__"
  
    def validate(self, data):
        username = data.get("username")
        phone = data.get("phone")

        if Person.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        if len(str(phone)) != 10:
            raise ValidationError("Phone number is not valid")
        return data

    def create(self, validated_data):
        contact = Contact.objects.create(**validated_data)
        return contact


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"

