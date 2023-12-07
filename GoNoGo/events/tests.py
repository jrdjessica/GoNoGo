from django.test import TestCase
from django.urls import reverse
from .models import Event
from django.contrib.auth.models import User


class EventTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(username='organizer_user')
        User.objects.create(username='attendee1')
        User.objects.create(username='attendee2')

    def setUp(self):
        # Set up modified objects used by individual test methods
        organizer = User.objects.get(username='organizer_user')
        event = Event.objects.create(
            id=1,
            title='Test Event',
            content='Test content',
            location='Test location',
            date='2024-01-01',
            time='12:00:00',
            decision=True,
            organizer=organizer
        )
        attendee1 = User.objects.get(username='attendee1')
        attendee2 = User.objects.get(username='attendee2')
        event.attendees.add(attendee1)

    def test_attendees_added(self):
        event = Event.objects.get(id=1)
        attendee1 = User.objects.get(username='attendee1')
        self.assertIn(attendee1, event.attendees.all())

    def test_attendees_count(self):
        event = Event.objects.get(id=1)
        self.assertEqual(event.attendees.count(), 1)

    def test_add_attendee(self):
        event = Event.objects.get(id=1)
        attendee2 = User.objects.get(username='attendee2')
        event.attendees.add(attendee2)
        self.assertIn(attendee2, event.attendees.all())
        self.assertEqual(event.attendees.count(), 2)


class EditEventViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(username='organizer_user')
        User.objects.create(username='attendee1')

    def setUp(cls):
        organizer = User.objects.get(username='organizer_user')
        event = Event.objects.create(
            id=2,
            title='Test Event',
            content='Test content',
            location='Test location',
            date='2024-01-01',
            time='12:00:00',
            decision=True,
            organizer=organizer
        )
        attendee1 = User.objects.get(username='attendee1')
        event.attendees.add(attendee1)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/dashboard/event/2/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('edit_event', args=[2]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('edit_event', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit.html')

    def test_past_date_event_create_error(self):
        organizer = User.objects.get(username='organizer_user')
        attendee1 = User.objects.get(username='attendee1')
        post_data = {
            'title': 'Test Event',
            'content': 'Test content',
            'location': 'Test location',
            'date': '2020-01-01',
            'time': '12:00:00',
            'decision': True,
            'organizer': organizer.id,
            'attendees': [attendee1.id],
        }
        response = self.client.post(reverse('new_event'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, 'form', None, 'The event time is in the past. Please choose a future date and time.')
