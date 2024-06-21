from django.test import TestCase
from todo_app.forms import TodoItemForm
from todo_app.models import Category, Priority, TodoItem

class TodoItemFormTest(TestCase):

    def setUp(self):
        # Create sample data for testing
        self.category_personal = Category.objects.create(name='Personal')
        self.category_work = Category.objects.create(name='Work')
        self.priority_high = Priority.objects.create(name='High')
        self.priority_low = Priority.objects.create(name='Low')

    def test_form_with_categories_and_priorities(self):
        # Test form initialization with custom categories and priorities
        custom_categories = Category.objects.filter(name__in=['Personal', 'Work'])
        custom_priorities = [(p.id, p.name) for p in Priority.objects.all()]

        form = TodoItemForm(categories=custom_categories, priorities=custom_priorities)

        self.assertEqual(len(form.fields['category'].queryset), 2)
        self.assertEqual(len(form.fields['priority'].choices), len(custom_priorities))

    def test_form_valid_data(self):
        # Test valid form data
        form_data = {
            'title': 'Test Todo',
            'description': 'Testing TodoItemForm',
            'checked': False,
            'date': '2024-06-25',  
            'category': self.category_personal.id,
            'priority': self.priority_high.id,
            'is_private': True,
        }
        form = TodoItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        # Test invalid form data (e.g., missing required fields)
        form_data = {
            'title': '',  
            'description': 'Testing TodoItemForm',
            'checked': False,
            'date': '2024-06-25',  
            'category': '',  
            'priority': self.priority_high.id,
            'is_private': True,
        }
        form = TodoItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('category', form.errors)
