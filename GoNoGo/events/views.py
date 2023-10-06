from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .event_form import EventForm
from .models import Event, Attendance
from django.contrib.auth.models import User
from django.db.models import Q



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
        

    events_combined = Event.objects.filter(Q(organizer=owner_id) | Q(attendees=owner_id))


    events_context["events_info"] = events_combined
   
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
        actual_user = request.user
        owner = User.objects.get(email=actual_user.email)
        event_id = request.POST.get('event_id', None)
        event_decision = request.POST.get('btn_value', None)
        if event_decision == "true":
            
            event_decision_bool = True
        else:
            event_decision_bool = False
        event = Event.objects.get(id=event_id)

        attendance = Attendance(user=owner, event=event, individual_decision=event_decision_bool)
        attendance.save()
        
        print("Attendance saved.", '$$$$$$$$$$$$$$$$$$$$')

        print("****************************")
    return redirect('/dashboard/')