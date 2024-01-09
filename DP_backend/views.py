from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
import secrets
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
# Create your views here.
# dp_backend/views.py


from .serializers import UserSerializer, UserSignupSerializer, UserLoginSerializer

class UserSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserSignupSerializer(data=request.data)
        verification_code = secrets.token_hex(3)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data["password"])
            user.save()
            Token.objects.get_or_create(user=user)
            dynamic_data = {
                'name' : user.username,
                'code' : verification_code
            }
            html_content = render_to_string("email.html",dynamic_data)
            plain_message = strip_tags(html_content)
            # send_mail("Welcome to The App",html_content, settings.EMAIL_HOST_USER, [user.email],fail_silently=False)
            message = EmailMultiAlternatives(subject="Welcome to the App",body=plain_message, from_email=settings.EMAIL_HOST_USER, to=[user.email])
            message.attach_alternative(html_content, "text/html")
            message.send()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
