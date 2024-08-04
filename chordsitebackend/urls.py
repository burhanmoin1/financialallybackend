from django.contrib import admin
from django.urls import path
from chordsiteapis.views import *

urlpatterns = [
    path('api/createuser/', UserCreateView.as_view(), name='user-create'),
]
