from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import TodoItem, Category


class TodoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name=Category.WORK)
        self.todo_item = TodoItem.objects.create(
            title='Test Todo',
            description='This is a test todo item.',
            checked=False,
            owner=self.user,
            category=self.category
        )
        self.client.login(username='testuser', password='testpass')

    def test_home_view(self):
        response = self.client.get(reverse('todo_app:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_app/home.html')

    def test_todo_list_view(self):
        response = self.client.get(reverse('todo_app:todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_app/todo_list.html')
        self.assertEqual(len(response.context['todolist']), 1)

    def test_todo_list_view_post(self):
        response = self.client.post(reverse('todo_app:todo_list'), {'checked': [self.todo_item.id]})
        self.assertRedirects(response, reverse('todo_app:todo_list'))
        self.todo_item.refresh_from_db()
        self.assertTrue(self.todo_item.checked)

    def test_todo_item_create_get(self):
        response = self.client.get(reverse('todo_app:todo_item_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_app/create_todo_item.html')

    def test_todo_item_create_post(self):
        response = self.client.post(reverse('todo_app:todo_item_create'), {
            'title': 'New Todo',
            'description': 'New description',
            'checked': False,
            'date': '', 
            'category': self.category.id
        })
        self.assertRedirects(response, reverse('todo_app:todo_list'))
        self.assertEqual(TodoItem.objects.count(), 2)

    def test_edit_todo_item_get(self):
        response = self.client.get(reverse('todo_app:todo_item_edit', args=[self.todo_item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_app/edit_todo_item.html')

    def test_edit_todo_item_post(self):
        response = self.client.post(reverse('todo_app:todo_item_edit', args=[self.todo_item.id]), {
            'title': 'Updated Todo',
            'description': 'Updated description',
            'checked': False,
            'date': '',  
            'category': self.category.id
        })
        self.assertRedirects(response, reverse('todo_app:todo_list'))
        self.todo_item.refresh_from_db()
        self.assertEqual(self.todo_item.title, 'Updated Todo')

    def test_delete_todo_item_get(self):
        response = self.client.get(reverse('todo_app:todo_item_delete', args=[self.todo_item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_app/confirm_delete.html')

    def test_delete_todo_item_post(self):
        response = self.client.post(reverse('todo_app:todo_item_delete', args=[self.todo_item.id]))
        self.assertRedirects(response, reverse('todo_app:todo_list'))
        self.assertEqual(TodoItem.objects.count(), 0)