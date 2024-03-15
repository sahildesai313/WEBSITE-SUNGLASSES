from rest_framework import serializers

from django.core.exceptions import ValidationError

from .models import *
import re
from typing import Union



class PersonSerializer(serializers.ModelSerializer):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    class Meta:
        model = Person
        fields = "__all__"
    
    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        confirmpassword=data.get("confirmpassword")
        phone = data.get("phone")

        if Person.objects.filter(username=username).exists():
            raise ValidationError('Username is allready exists')
        if len(str(phone)) != 10:
            raise ValidationError("phone number is not valid")
        if password != confirmpassword:
            raise ValidationError('password not match')
        return data
    
    def create(self, validated_data):
        gender = validated_data.pop("gender")
        validated_data["gender"] = gender.lower()
        person_details= Person.objects.create(**validated_data)
        person_details.save()
        return person_details




class Loginserializer(serializers.ModelSerializer):

    class Meta:
        model= Person
        fields = ('username', 'password')

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        person_details =  Person.objects.filter(username=username,password=password).first()
        if not person_details:
            raise ValidationError("Invalid Username or Password")
        return data
       

class Forgetserializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('email',)

    def validate(self, data):
        email = data.get("email")
        person_details = Person.objects.filter(email=email)
        if not person_details:
            raise serializers.ValidationError("email address not valid")
        return data


class ResetSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Person
        fields = ('password', 'confirmpassword')

    def validate(self, data):
        email = self.context.get('email_id')
        password = data.get('password')
        cpassword = data.get('confirmpassword')

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
        if otp != enter_otp :
            raise serializers.ValidationError("Invalid OTP")
        return data

    

class ChangeSerializer(serializers.ModelSerializer):


    class Meta:
        model = Person
        fields = ('password', 'confirmpassword')

    def validate(self, data):
        username =self.context.get('user_id')
        password = data.get('password')
        confirmpassword = data.get('confirmpassword')

        if password != confirmpassword:
            raise ValidationError("password not match")
        
        person_details = Person.objects.get(username=username)
        person_details.password = password
        person_details.confirmpassword = confirmpassword
        person_details.save()
        data['person_details'] = person_details
        return data

class EditProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('fullname','phone', 'country',)

    def validate(self, data):
        username = self.context.get('user_id')
        fullname = data.get('fullname')
        phone = data.get('phone')
        country = data.get('country')
        person_details = Person.objects.filter(username=username).first()
        phone_number = re.findall("[a-z]",phone)
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
        fields= ('city', 'state', 'address', 'locality', 'pincode')


    def create(self, validated_data):
        username  = self.context.get('username')
        person = Person.objects.filter(username = username).first()
        address = Address.objects.get_or_create(person=person, **validated_data)
        return address
    

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = '__all__'

    # def validate(self, data):
    #     cardno = data.get('Cardno')
    #     cvv = data.get('Cvv')
    #     card_no = re.findall("[a-z]",cardno)
    #     cvv_no = re.findall("[a-z]",cvv)
    #     if (card_no) or (cvv_no) or (len(cardno) != 12) or (len(cvv) != 3) :
    #         raise ValidationError("Enter Valid Carddeatils ")
    #     return data
    
    def create(self, validated_data):
    #     pincode = self.context.get('pincode')
    #     address = Address.objects.filter(pincode = pincode).first()
          card = Address.objects.create(**validated_data)
          return card