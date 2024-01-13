from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "username", "location", "phone_number", "weight", "height", "bmi"]

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "username", "password", "phone_number"]
        extra_kwargs = {"password": {"write_only": True}}

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ActivationSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = ['activation_code']

class ResetSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
