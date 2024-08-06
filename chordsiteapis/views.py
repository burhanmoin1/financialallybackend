from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
import uuid
from django.utils.crypto import get_random_string
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from .mongobackend import MongoEngineUserBackend

# signup API
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        activation_token = str(uuid.uuid4().hex)
        serializer.save(activation_token=activation_token)

@api_view(['GET'])
def check_activation_token_validity(request, activation_token):
    try:
        # Find the user with the given activation token
        user = User.objects.get(activation_token=activation_token)
        
        if user.activation_token_valid:
            return Response({'valid': True, 'message': 'Activation token is valid.'}, status=200)
        else:
            return Response({'valid': False, 'message': 'Activation token has already been used.'}, status=400)
    
    except User.DoesNotExist:
        return Response({'valid': False, 'message': 'Activation token is invalid.'}, status=404)
    except Exception as e:
        return Response({'valid': False, 'message': str(e)}, status=500)

@api_view(['POST'])
def verify_activation(request, activation_token):
    print(f"Received token: {activation_token}")  # Debugging line

    try:
        # Find the user with the given activation token
        user = User.objects.get(activation_token=activation_token)
        print(f"Found user: {user.email}, Token valid: {user.activation_token_valid}")  # Debugging line
        
        # Check if the activation token is valid
        if user.activation_token_valid:
            # Update user fields
            user.is_activated = True
            user.activation_token_valid = False
            user.save()
            
            # Return a JSON response indicating success
            return Response({'success': True, 'message': 'Your account has been activated successfully!'}, status=200)
        else:
            # Token is not valid, return a 400 response with an error message
            return Response({'success': False, 'message': 'Account is already activated.'}, status=400)
    
    except User.DoesNotExist:
        # User with the given token does not exist, return a 404 response with an error message
        return Response({'success': False, 'message': 'Activation token is not valid.'}, status=404)
    except Exception as e:
        # Handle unexpected errors
        return Response({'success': False, 'message': str(e)}, status=500)


@api_view(['POST'])
def generate_password_reset_token(request):
    try:
        # Extract email from the request
        email = request.data.get('email')

        # Find the user by email
        user = User.objects.get(email=email)
        
        # Generate a unique token
        token = uuid.uuid4().hex
        
        # Update user document with the token and set it as valid
        user.password_reset_token = token
        user.password_reset_token_valid = True
        user.save()
        
        # Optionally, you can send an email with the token to the user
        
        return JsonResponse({'message': 'Password reset token generated successfully', 'token': token}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User with this email does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


class ValidateTokenView(View):
    def get(self, request, reset_token):
        try:
            # Find the user by password reset token
            user = User.objects.get(password_reset_token=reset_token, password_reset_token_valid=True)
            return JsonResponse({'valid': True}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'valid': False, 'error': 'Invalid or expired password reset token'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class ResetPasswordView(View):
    def post(self, request, reset_token):
        try:
            # Extract new password from the request
            new_password = request.POST.get('password')

            # Find the user by password reset token
            user = User.objects.get(password_reset_token=reset_token, password_reset_token_valid=True)

            # Hash the new password
            hashed_password = make_password(new_password)

            # Update user document with the new password and invalidate the token
            user.password = hashed_password
            user.password_reset_token = ''
            user.password_reset_token_valid = False
            user.save()

            return JsonResponse({'message': 'Password has been reset successfully'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid or expired password reset token'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def login_user_api(request):
    # Extract data from the request
    data = request.data
    email = data.get('email')
    password = data.get('password')

    # Authenticate the user
    user = MongoEngineUserBackend().authenticate(request, email=email, password=password)

    # Check if the user is authenticated and activated
    if user is not None and user.is_activated:
        session_token = str(uuid.uuid4())

        # Update the user's session tokens (max 4)
        user.session_tokens.append(session_token)
        if len(user.session_tokens) > 4:
            user.session_tokens.pop(0)  # Remove the oldest session token if there are more than 4
        user.save()

        # Respond with success message and session token
        return Response({
            'message': 'Login successful',
            'name': user.first_name,
            'user_email': user.email,
            'session_token': session_token
        }, status=status.HTTP_200_OK)
    else:
        # Authentication failed or account not activated
        return Response({
            'error': 'Invalid email or password, or account not activated. Please check activation email.'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_session_checker(request):
    data = request.data
    email = data.get('email')
    session_token = data.get('session_token')

    if not email or not session_token:
        return Response({'error': 'Email and session token are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch the user based on the provided email
        user = User.objects.get(email=email)

        # Check if the session token exists in the user's session tokens
        if session_token in user.session_tokens:
            return Response({'message': 'Session authenticated'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Session not authenticated'}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)