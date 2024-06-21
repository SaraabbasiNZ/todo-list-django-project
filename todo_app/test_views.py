from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import TodoItem, Category, Priority


class TodoItemViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create test data: categories and priorities
        self.category_personal = Category.objects.create(name='Personal')
        self.category_work = Category.objects.create(name='Work')
        self.priority_high = Priority.objects.create(name='High')
        self.priority_medium = Priority.objects.create(name='Medium')

        # Create a test TodoItem
        self.todo_item1 = TodoItem.objects.create(
            title='Test Todo',
            description='Test Description',
            owner=self.user,
            date=timezone.now() + timedelta(days=1),
            category=self.category_personal,
            priority=self.priority_high,
            is_private=False
        )

    def test_home_view(self):
        response = self.client.get(reverse('todo_app:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_app/home.html')

    def test_todo_list_view_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('todo_app:todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_app/todo_list.html')

    def test_todo_list_view_post(self):
        self.client.force_login(self.user)
        data = {'checked': [self.todo_item1.id]}
        response = self.client.post(reverse('todo_app:todo_list'), data)
        self.assertEqual(response.status_code, 302)

        # Check if the todo_item1 is checked in the database
        self.todo_item1.refresh_from_db()
        self.assertTrue(self.todo_item1.checked)

    def test_todo_item_create_view_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('todo_app:todo_item_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_app/create_todo_item.html')

    def test_todo_item_create_view_post_valid(self):
        self.client.force_login(self.user)
        data = {
            'title': 'New Todo',
            'description': 'New Description',
            'date': timezone.now() + timedelta(days=3),
            'category': self.category_work.id,
            'priority': self.priority_medium.id,
            'is_private': True
        }
        response = self.client.post(reverse('todo_app:todo_item_create'), data)
        self.assertEqual(response.status_code, 302)

        # Check if the TodoItem is created in the database
        new_todo_item = TodoItem.objects.get(title='New Todo')
        self.assertIsNotNone(new_todo_item)
        self.assertEqual(new_todo_item.description, 'New Description')

    def test_edit_todo_item_view_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('todo_app:todo_item_edit', args=[self.todo_item1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_app/edit_todo_item.html')

    def test_edit_todo_item_view_post_valid(self):
        self.client.force_login(self.user)
        data = {
            'title': 'Updated Todo',
            'description': 'Updated Description',
            'date': timezone.now() + timedelta(days=2),
            'category': self.category_work.id,
            'priority': self.priority_medium.id,
            'is_private': True
        }
        response = self.client.post(reverse('todo_app:todo_item_edit', args=[self.todo_item1.id]), data)
        self.assertEqual(response.status_code, 302)

        # Check if the TodoItem is updated in the database
        self.todo_item1.refresh_from_db()
        self.assertEqual(self.todo_item1.title, 'Updated Todo')
        self.assertEqual(self.todo_item1.description, 'Updated Description')

    def test_delete_todo_item_view_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('todo_app:todo_item_delete', args=[self.todo_item1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_app/confirm_delete.html')

    def test_delete_todo_item_view_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('todo_app:todo_item_delete', args=[self.todo_item1.id]))
        self.assertEqual(response.status_code, 302)

        # Check if the TodoItem is deleted from the database
        self.assertFalse(TodoItem.objects.filter(id=self.todo_item1.id).exists())

    