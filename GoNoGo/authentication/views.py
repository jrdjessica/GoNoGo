from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
import json

from .models import User
from .serializers import UserSerializer


class Users(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        # Parse the JSON payload
        data = json.loads(request.body.decode('utf-8'))

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')

        # Validate the data (you can add more robust validation here)
        if not all([first_name, last_name, email, password]):
            return JsonResponse({'message': 'Invalid data'}, status=400)

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({'message': 'Email already exists'}, status=400)

        # Create a new user
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        return JsonResponse({'message': 'Account created successfully'}, status=201)

    return JsonResponse({'message': 'Only POST method is allowed'}, status=405)