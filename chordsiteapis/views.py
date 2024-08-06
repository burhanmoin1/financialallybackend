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

#verify user API
@require_http_methods(["GET"])
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
            return JsonResponse({'success': True, 'message': 'Your account has been activated successfully!'}, status=200)
        else:
            # Token is not valid, return a 400 response with an error message
            return JsonResponse({'success': False, 'message': 'Account is already activated.'}, status=400)
    
    except User.DoesNotExist:
        # User with the given token does not exist, return a 404 response with an error message
        return JsonResponse({'success': False, 'message': 'Activation token is not valid.'}, status=404)


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

