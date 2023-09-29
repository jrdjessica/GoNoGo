from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .event_form import EventForm
from .models import Event
from django.contrib.auth.models import User



@login_required(login_url='/', redirect_field_name='next')
def events_dashboard(request):
    return render(request, "dashboard.html")


def new_event(request):
    context = {}
    if request.user.is_authenticated:
        if hasattr(request.user, '_wrapped'):
            actual_user = request.user._wrapped
        else:
            actual_user = request.user
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            location = form.cleaned_data.get('location')
            date = form.cleaned_data.get('date')
            time = form.cleaned_data.get('time')
            attendees = form.cleaned_data.get('attendees')
            try:
                attendee = User.objects.get(email=attendees)
                attendee_id = attendee.id
            except User.DoesNotExist:
                attendee_id = None

            event = Event(title=title, content=content, location=location, date=date, time=time, decision = True, organizer=actual_user)
            event.save()
            event.attendees.add(attendee_id)
            event.save()
            return redirect('dashboard/') 
        else:
            context['error'] = 'Invalid form'
    else:
        form = EventForm()

    context['form'] = form
    return render(request, "create_event.html", context)