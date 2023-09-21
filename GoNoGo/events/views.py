from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='/', redirect_field_name='next')
def events_dashboard(request):
    print("run ******************")
    return render(request, "dashboard.html")