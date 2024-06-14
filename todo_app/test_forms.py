from django.test import TestCase
from django.utils import timezone
from .forms import TodoItemForm
from .models import TodoItem, Category
from datetime import timedelta

class TodoItemFormTest(TestCase):
    def setUp(self):
        # Set up initial data for categories
        self.category1 = Category.objects.create(name='Work')
        self.category2 = Category.objects.create(name='Personal')

    def test_valid_form(self):
        data = {
            'title': 'Test Todo',
            'description': 'This is a test todo.',
            'checked': False,
            'date': timezone.now() + timedelta(days=1),
            'category': self.category1.id
        }
        form = TodoItemForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_past_date(self):
        past_date = timezone.now() - timedelta(days=1)
        data = {
            'title': 'Test Todo',
            'description': 'This is a test todo with a past date.',
            'checked': False,
            'date': past_date,
            'category': self.category1.id
        }
        form = TodoItemForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        self.assertEqual(form.errors['date'], ['Please enter a date from today or the future.'])

    def test_invalid_form_missing_category(self):
        data = {
            'title': 'Test Todo',
            'description': 'This is a test todo without a category.',
            'checked': False,
            'date': timezone.now() + timedelta(days=1),
        }
        form = TodoItemForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)
        self.assertEqual(form.errors['category'], ['This field is required.'])

    def test_custom_category_queryset(self):
        custom_categories = Category.objects.filter(name='Personal')
        form = TodoItemForm(categories=custom_categories)
        self.assertEqual(list(form.fields['category'].queryset), list(custom_categories))

    def test_valid_form_with_custom_category_queryset(self):
        custom_categories = Category.objects.filter(name='Personal')
        data = {
            'title': 'Test Todo',
            'description': 'This is a test todo.',
            'checked': False,
            'date': timezone.now() + timedelta(days=1),
            'category': custom_categories.first().id
        }
        form = TodoItemForm(data=data, categories=custom_categories)
        self.assertTrue(form.is_valid())