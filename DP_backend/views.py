from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
import secrets
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
# Create your views here.
# dp_backend/views.py
from django.contrib.auth.hashers import check_password

from .serializers import UserSerializer, UserSignupSerializer, UserLoginSerializer, ActivationSerializer, ResetSerializer

class UserSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserSignupSerializer(data=request.data)
        verification_code = secrets.token_hex(3)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data["password"])
            user.activation_code = verification_code
            user.save()
            token = Token.objects.get_or_create(user=user)
            dynamic_data = {
                'name' : user.username,
                'code' : verification_code
            }
            html_content = render_to_string("email.html",dynamic_data)
            plain_message = strip_tags(html_content)
            message = EmailMultiAlternatives(subject="Welcome to the App",body=plain_message, from_email=settings.EMAIL_HOST_USER, to=[user.email])
            message.attach_alternative(html_content, "text/html")
            #Login the users
            auth_user = authenticate(request, email=serializer.validated_data["email"], password=serializer.validated_data["password"])
            if auth_user:
                login(request, auth_user)
                token, created = Token.objects.get_or_create(user = auth_user)
                message.send()
                # verify the verificaation code
                

            return Response({"data" : serializer.data , "token" : token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, email=serializer.validated_data["email"], password=serializer.validated_data["password"])
            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class ActivationView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.activation_code == request.data['activation_code']:
                user.activated = True
                user.save()
                return Response({"success": True})
        return Response({"erroor":"Enter the activation code"})

class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        serializer = ResetSerializer(data = request.data)
        if serializer.is_valid():
            user = request.user
            if check_password(request.data["old_password"], user.password):
                user.set_password(request.data["password"])
                user.save()
                return Response({"message":"Password Changed Succesfully"})
            else:
                return Response({"message":"Password doesnot match"})
        return Response(serializer.errors)


            