from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.parsers import MultiPartParser
import secrets
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

import os
import random

from django.contrib.auth.hashers import check_password
from .models import CustomUser, Disease
from .serializers import UserSerializer, UserSignupSerializer, UserLoginSerializer, EyePredictSerializer
# from .alogirthm.algorithm import predict_disease
from pathlib import Path
from DP_backend.alogirthm.eyepredict import predict
from DP_backend.alogirthm.pdf import generate_pdf_file
from django.http import FileResponse
BASE_DIR = Path(__file__).resolve().parent.parent
class UserSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserSignupSerializer(data=request.data)
        # verification_code = secrets.token_hex(3)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data["password"])
            # user.activation_code = verification_code
            user.save()
            token = Token.objects.get_or_create(user=user)
            # dynamic_data = {
            #     'name' : user.username,
            #     'code' : verification_code
            # }
            # html_content = render_to_string("email.html",dynamic_data)
            # plain_message = strip_tags(html_content)
            # message = EmailMultiAlternatives(subject="Welcome to the App",body=plain_message, from_email=settings.EMAIL_HOST_USER, to=[user.email])
            # message.attach_alternative(html_content, "text/html")
            #Login the users
            # auth_user = authenticate(request, email=serializer.validated_data["email"], password=serializer.validated_data["password"])
            # if auth_user:
            #     login(request, auth_user)
            #     token, created = Token.objects.get_or_create(user = auth_user)
            #     message.send()
                # verify the verificaation code
                

            return Response({"data" : serializer.data, "token" : token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, username=serializer.validated_data["username"], password=serializer.validated_data["password"])
            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
class EyeDiseasePredictionView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    
    def generate_pdf(self,user):
        response = FileResponse(generate_pdf_file(user),as_attachment=True, filename="report.pdf")
        return response
    def post(self, request):
        user = self.request.user
        disease = Disease.objects.get_or_create(user_id=user.id)
        serializer = EyePredictSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            file_path = os.path.join(settings.MEDIA_ROOT, image.name)
            with open(file_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            # image_path = self.save_image(image)
        # if request.FILES.get('image'):
            # image = request.FILES['image']
            predictions = predict(file_path)
            if user:
                disease, created = Disease.objects.get_or_create(user=user)
                
                disease.dname = predictions
                disease.image = file_path
                    
                disease.save()
            
            return Response({"predictions" : predictions, "path" : file_path})
        else:
            return Response({
                "error":"No image received"
            })
            
    # def save_image(self, image):
    #     # Define the path to save the image
    #     save_path = os.path.join(BASE_DIR, 'media')
    #     # Save the image to the specified path
    #     with open(save_path, 'wb') as f:
    #         for chunk in image.chunks():
    #             f.write(chunk)
    #     return save_path
        