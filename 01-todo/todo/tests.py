from django.test import TestCase, Client
from django.urls import reverse
from .models import Todo
from datetime import datetime, timedelta


class TodoModelTest(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(
            title='Test TODO',
            description='Test Description',
            due_date=datetime.now() + timedelta(days=1)
        )

    def test_todo_creation(self):
        self.assertEqual(self.todo.title, 'Test TODO')
        self.assertFalse(self.todo.completed)

    def test_todo_str(self):
        self.assertEqual(str(self.todo), 'Test TODO')


class TodoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(title='Test TODO')

    def test_todo_list_view(self):
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('todos', response.context)

    def test_create_todo(self):
        response = self.client.post(reverse('create_todo'), {
            'title': 'New TODO',
            'description': 'New Description',
        })
        self.assertEqual(Todo.objects.count(), 2)

    def test_toggle_todo(self):
        response = self.client.post(reverse('toggle_todo', args=[self.todo.pk]))
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.completed)

    def test_delete_todo(self):
        response = self.client.post(reverse('delete_todo', args=[self.todo.pk]))
        self.assertEqual(Todo.objects.count(), 0)
