from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, TodoItem

class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name=Category.PERSONAL)

    def test_category_creation(self):
        self.assertIsInstance(self.category, Category)
        self.assertEqual(self.category.name, 'Personal')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Personal')

    def test_category_choices(self):
        choices = [Category.PERSONAL, Category.WORK, Category.STUDY, Category.HEALTH, Category.HOME, Category.OTHER]
        for choice in choices:
            category = Category(name=choice)
            category.full_clean()
            self.assertEqual(category.name, choice)


class TodoItemModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name=Category.WORK)
        self.todo_item = TodoItem.objects.create(
            title='Test Todo',
            description='This is a test todo item.',
            checked=False,
            owner=self.user,
            date=None,
            category=self.category
        )

    def test_todo_item_creation(self):
        self.assertIsInstance(self.todo_item, TodoItem)
        self.assertEqual(self.todo_item.title, 'Test Todo')
        self.assertEqual(self.todo_item.description, 'This is a test todo item.')
        self.assertFalse(self.todo_item.checked)
        self.assertEqual(self.todo_item.owner, self.user)
        self.assertIsNone(self.todo_item.date)
        self.assertEqual(self.todo_item.category, self.category)

    def test_todo_item_str(self):
        self.assertEqual(str(self.todo_item), 'Test Todo')

    def test_todo_item_foreign_key_user(self):
        self.assertEqual(self.todo_item.owner.username, 'testuser')

    def test_todo_item_foreign_key_category(self):
        self.assertEqual(self.todo_item.category.name, 'Work')

    def test_todo_item_toggle_checked(self):
        self.todo_item.checked = True
        self.todo_item.save()
        self.assertTrue(self.todo_item.checked)