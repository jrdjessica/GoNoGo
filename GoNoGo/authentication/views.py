from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .forms import LogInForm, SignUpForm
from .models import User
from django.contrib import messages


import json

from .models import User
from .serializers import UserSerializer


def home_view(request):
    next_url = request.GET.get('next')
    if next_url == '/dashboard/':  
        messages.warning(request, 'You need to login to access the dashboard.')
    context ={}
    
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user = User.objects.get(email=email)
                if user.password == password: 
                    return redirect('dashboard/')  
                else:
                    context['error'] = 'Incorrect password'
            except User.DoesNotExist:
                context['error'] = 'User does not exist'
        else:
            context['error'] = 'Invalid form'
    else:
        form = LogInForm()

    context['form'] = form
    return render(request, "home.html", context)


def signup_view(request):
    context = {}
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            # Create user 
            user = User(email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
            return redirect('dashboard/') 
        else:
            context['error'] = 'Invalid form'
    else:
        form = SignUpForm()

    context['form'] = form
    return render(request, "signup.html", context)

class Users(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer