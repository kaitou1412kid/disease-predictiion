# dp_backend/urls.py

from django.urls import path, include
from .views import UserSignupView, UserLoginView, ActivationView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('activate/', ActivationView.as_view(), name='user-activate'),
    # Add other URLs as needed
]
