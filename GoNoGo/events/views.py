from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .event_form import EventForm
from .models import Event



@login_required(login_url='/', redirect_field_name='next')
def events_dashboard(request):
    print("run ******************")
    return render(request, "dashboard.html")


def new_event(request):
    context = {}
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            location = form.cleaned_data.get('location')
            date = form.cleaned_data.get('date')
            time = form.cleaned_data.get('time')
            attendees = form.cleaned_data.get('attendees')

            # Create event 
            event = Event(title=title, content=content, location=location, date=date, time=time, attendees= attendees)
            event.save()
            return redirect('dashboard/') 
        else:
            context['error'] = 'Invalid form'
    else:
        form = EventForm()

    context['form'] = form
    return render(request, "create_event.html", context)