from django.contrib import admin
from django.urls import path
from chordsiteapis.views import *

urlpatterns = [
    path('api/createuser/', UserCreateView.as_view(), name='user-create'),
    path('api/verify/<str:activation_token>/', verify_activation, name='verify_activation'),
    path('api/generate_password_reset_token/', generate_password_reset_token, name='generate_password_reset_token'),
    path('api/validate_token/<str:reset_token>/', ValidateTokenView.as_view(), name='validate_token'),
    path('api/reset_password/<str:reset_token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('api/check-token-validity/${activation_token}/', check_activation_token_validity, name='check_verification_token_validatity'),
    path('api/loginuser/', login_user_api, name='login_user'),
    path('api/user_session_checker/', user_session_checker, name='user_session_checker')
]
