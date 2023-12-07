from django.test import TestCase
from .models import User
from .forms import LogInForm


class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(first_name='Big', last_name='Bob',
                            email='anyemail@gmail.com', password='1234455555')

    def test_first_name_label(self):
        user = User.objects.get(id=1)
        field_label = User._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_first_name_max_length(self):
        user = User.objects.get(id=1)
        max_length = User._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 50)


class LoginFormTest(TestCase):

    def test_valid_data(self):
        form = LogInForm(data={
            'email': 'user@example.com',
            'password': 'securepassword123',
        })
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = LogInForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'email': ['This field is required.'],
            'password': ['This field is required.'],
        })

    def test_field_placeholder(self):
        form = LogInForm()
        self.assertEqual(
            form.fields['email'].widget.attrs['placeholder'], 'Your Email')
        self.assertEqual(
            form.fields['password'].widget.attrs['placeholder'], 'Your Password')
