from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .event_form import EventForm
from .models import Event, Attendance
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime, timedelta
import random


@login_required(login_url='/', redirect_field_name='next')
def events_dashboard(request):

    events_context = {}
    now = datetime.now()
    within_24_hours = []
    past_events = []

    if hasattr(request.user, '_wrapped'):
        actual_user = request.user._wrapped
    else:
        actual_user = request.user

    if request.method == 'GET':

        owner_email = User.objects.get(email=actual_user)
        owner_id = owner_email.id

    events_combined = Event.objects.filter(
        Q(organizer=owner_id) | Q(attendees=owner_id)).distinct()

    events_combined = sorted(
        events_combined, key=lambda event: (event.date, event.time))

    for event in events_combined:
        event_time_date = datetime.combine(event.date, event.time)
        if now + timedelta(hours=24) > event_time_date > now:
            within_24_hours.append(True)
        else:
            within_24_hours.append(False)
    for event in events_combined:
        event_time_date = datetime.combine(event.date, event.time)
        if event_time_date < now:
            past_events.append(True)
        else:
            past_events.append(False)

    events_context["events_info"] = zip(
        events_combined, within_24_hours, past_events)

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

            input_time = datetime.combine(date, time)

            to_validate_time = datetime.now() + timedelta(days=1)

            if datetime.today() > input_time:
                form.add_error(
                    None, 'The event time is in the past. Please choose a future date and time.')
                context['form'] = form

                return render(request, "create_event.html", context)
            elif to_validate_time > input_time:
                form.add_error(
                    None, 'The event time is within 24 hours. Please choose a different date and time.')
                context['form'] = form

                return render(request, "create_event.html", context)
            else:
                event = Event(title=title, content=content, location=location,
                              date=date, time=time, decision=False, organizer=actual_user)
                event.save()

                for attendee in attendee_emails:
                    try:
                        event.attendees.add(attendee)

                    except Exception as e:
                        print(f"An error occurred while adding attendee: {e}")

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

        attendance, created = Attendance.objects.get_or_create(
            user=owner, event=event, defaults={'individual_decision': event_decision_bool})

        if not created:
            attendance.individual_decision = event_decision_bool
            attendance.save()

        going_attendees = Attendance.objects.filter(
            event_id=event_id, individual_decision=True).count()
        num_total_attendees = event.attendees.count()
        ratio = going_attendees / (num_total_attendees+1)
        rounded_ratio = round(ratio, 2)
        if rounded_ratio > 0.5:
            event.decision = True
        elif rounded_ratio == 0.5:
            event.decision = random.choice([True, False])
        else:
            event.decision = False

        print(num_total_attendees, event.decision)

    return redirect('/dashboard/')


def edit(request, id):

    event_instance = get_object_or_404(Event, id=id)

    if request.method == 'POST':

        form = EventForm(request.POST, instance=event_instance)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/')

    else:

        form = EventForm(instance=event_instance)

    context = {'form': form}
    context['id'] = id

    return render(request, "edit.html", context)


def delete(request, id):
    event = Event.objects.get(id=id)
    event.delete()
    return redirect('/dashboard/')


def log_out(request):
    return redirect('/')


def past_events(request):
    events_context = {}
    now = datetime.now()
    past_events = []

    if request.method == 'GET':
        actual_user = request.user
        owner_email = User.objects.get(email=actual_user.email)

        owner_id = owner_email.id
    events_combined = Event.objects.filter(
        Q(organizer=owner_id) | Q(attendees=owner_id)).distinct()
    for event in events_combined:
        event_time_date = datetime.combine(event.date, event.time)
        if event_time_date < now:
            past_events.append(True)
        else:
            past_events.append(False)
    events_context["events_info"] = zip(events_combined, past_events)

    return render(request, "past_events.html", events_context)
