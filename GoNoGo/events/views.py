from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/', redirect_field_name='next')
def events_dashboard(request):
    print("run ******************")
    return render(request, "dashboard.html")