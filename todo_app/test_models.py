from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Category, Priority, TodoItem
from django.contrib.auth.models import User


class CategoryModelTest(TestCase):
    def test_category_str(self):
        # Test Category model __str__ method returns the name
        category = Category.objects.create(name='Work')
        self.assertEqual(str(category), 'Work')


class PriorityModelTest(TestCase):
    def test_priority_str(self):
        # Test Priority model __str__ method returns the name
        priority = Priority.objects.create(name='High')
        self.assertEqual(str(priority), 'High')


class TodoItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Work')
        self.priority = Priority.objects.create(name='High')

    def test_todoitem_str(self):
        # Test TodoItem model __str__ method returns the title
        todo_item = TodoItem.objects.create(
            title='Finish project',
            description='Complete the final draft of the project',
            owner=self.user,
            category=self.category,
            priority=self.priority
        )
        self.assertEqual(str(todo_item), 'Finish project')

    def test_is_public(self):
        # Test TodoItem is_public method returns correct boolean
        todo_item = TodoItem.objects.create(
            title='Public task',
            owner=self.user,
            category=self.category,
            priority=self.priority,
            is_private=False
        )
        self.assertTrue(todo_item.is_public())

        private_todo_item = TodoItem.objects.create(
            title='Private task',
            owner=self.user,
            category=self.category,
            priority=self.priority,
            is_private=True
        )
        self.assertFalse(private_todo_item.is_public())

    def test_save_with_past_date(self):
        # Test saving TodoItem with a past date raises ValidationError
        with self.assertRaises(ValidationError):
            past_date = timezone.now() - timezone.timedelta(days=1)
            TodoItem.objects.create(
                title='Past due task',
                owner=self.user,
                category=self.category,
                priority=self.priority,
                date=past_date
            )

    def test_save_with_future_date(self):
        # Test saving TodoItem with a future date sets the date correctly
        future_date = timezone.now() + timezone.timedelta(days=1)
        todo_item = TodoItem.objects.create(
            title='Future task',
            owner=self.user,
            category=self.category,
            priority=self.priority,
            date=future_date
        )
        self.assertEqual(todo_item.date, future_date)
