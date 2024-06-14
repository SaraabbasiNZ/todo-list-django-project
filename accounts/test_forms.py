from django.test import TestCase
from django.contrib.auth.models import User
from accounts.forms import CustomUserCreationForm

class CustomUserCreationFormTest(TestCase):
    def test_valid_form(self):
        # Create a form instance with valid data
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'test_password',
            'password2': 'test_password',
        }
        form = CustomUserCreationForm(data=form_data)

        # Assert that the form is valid
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        # Create a user with the same email
        User.objects.create_user(username='existing_user', email='test@example.com', password='password123')

        # Create a form instance with the same email
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'test_password',
            'password2': 'test_password',
        }
        form = CustomUserCreationForm(data=form_data)

        # Assert that the form is not valid due to email uniqueness
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_passwords_not_match(self):
        # Create a form instance with passwords that don't match
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'test_password',
            'password2': 'different_password',
        }
        form = CustomUserCreationForm(data=form_data)

        # Assert that the form is not valid
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)