from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .forms import LogInForm, SignUpForm
from django.contrib.auth import authenticate,login
from django.contrib import messages


import json


from .serializers import UserSerializer


def home_view(request):
    next_url = request.GET.get('next')
    if next_url == '/dashboard/':
        messages.warning(request, 'You need to login to access the dashboard.')
    context ={}

    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            print('***************If Valid**********************')
            email = request.POST['email']
            password = request.POST['password']
  
            print(email,password)
            try:
                print('start trying')
                user = authenticate(request, username=email, password=password)

                print(user)
                if user is not None: 
                    form = login(request, user)
                    print('**************Login***********************')
                    messages.success(request, f' welcome {email} !!')
                    return redirect('/dashboard/')
                else:
                    print("user is None~~~~~~~~~~~~~~~~~")
                    messages.info(request, f'account done not exit plz sign in')
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
            username = form.cleaned_data.get('email')

            # Create user 
            user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, username=username)
            user.save()
            #handle successfully log in 
            login(request, user)
            return redirect('/dashboard/') 
        else:
            context['error'] = 'Invalid form'
    else:
        form = SignUpForm()

    context['form'] = form
    return render(request, "signup.html", context)

class Users(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

