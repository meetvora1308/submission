import imp
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Address

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password',"groups","date_joined","user_permissions"]

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ["user",]