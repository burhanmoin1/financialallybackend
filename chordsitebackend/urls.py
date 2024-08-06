from django.contrib import admin
from django.urls import path
from chordsiteapis.views import *

urlpatterns = [
    path('api/createuser/', UserCreateView.as_view(), name='user-create'),
    path('api/verify/<str:activation_token>/', verify_activation, name='verify_activation'),
    path('api/generate_password_reset_token/', generate_password_reset_token, name='generate_password_reset_token'),
]
