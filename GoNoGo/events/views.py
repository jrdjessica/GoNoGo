from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .event_form import EventForm
from .models import Event
from django.contrib.auth.models import User



@login_required(login_url='/', redirect_field_name='next')
def events_dashboard(request):
    events_context = {}
    if hasattr(request.user, '_wrapped'):
        actual_user = request.user._wrapped
    else:
        actual_user = request.user
    if request.method == 'GET':

        owner_email = User.objects.get(email=actual_user)
        owner_id = owner_email.id
        events_info = Event.objects.filter(organizer=owner_id)
        



    events_context["events_info"] = events_info
    print(events_context)
    return render(request, "dashboard.html", events_context)


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
            attendee_emails = form.cleaned_data.get('attendees')
           
  

            event = Event(title=title, content=content, location=location, date=date, time=time, decision = True, organizer=actual_user)
            event.save()
            for email in attendee_emails:
                try:
                    attendee = User.objects.get(email=email.strip())
                    event.attendees.add(attendee)  
                except User.DoesNotExist:

                    print(f"User with email {email} does not exist.")
           
            event.save()
            return redirect('/dashboard/') 
        else:
            context['error'] = 'Invalid form'
    else:
        form = EventForm()

    context['form'] = form
    return render(request, "create_event.html", context)

def individual_decision(request):
    if request.method == 'POST':
        print("****************************")
    return redirect('/dashboard/')