from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "username", "location", "blood_group", "phone_number", "weight", "height", "bmi"]

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "username", "password", "phone_number"]
        extra_kwargs = {"password": {"write_only": True}}

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

# class ActivationSerializer(serializers.Serializer):
#     class Meta:
#         model = CustomUser
#         fields = ["activated"]
