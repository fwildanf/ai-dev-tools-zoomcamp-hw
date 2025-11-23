from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, timedelta
from .models import Todo, Category


class TodoModelTests(TestCase):
    """Test cases for Todo model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Work',
            description='Work-related tasks'
        )
    
    def test_create_todo_with_all_fields(self):
        """Test creating a todo with all fields."""
        todo = Todo.objects.create(
            title='Complete project',
            description='Finish the Django project',
            user=self.user,
            category=self.category,
            completed=False,
            due_date=datetime.now() + timedelta(days=1)
        )
        self.assertEqual(todo.title, 'Complete project')
        self.assertEqual(todo.user, self.user)
        self.assertEqual(todo.category, self.category)
        self.assertFalse(todo.completed)
    
    def test_create_todo_without_optional_fields(self):
        """Test creating a todo without optional fields."""
        todo = Todo.objects.create(
            title='Simple task',
            user=self.user
        )
        self.assertEqual(todo.title, 'Simple task')
        self.assertIsNone(todo.description)
        self.assertIsNone(todo.category)
        self.assertIsNone(todo.due_date)
    
    def test_todo_str_representation(self):
        """Test todo string representation."""
        todo = Todo.objects.create(
            title='Test Todo',
            user=self.user
        )
        self.assertEqual(str(todo), 'Test Todo')
    
    def test_todo_ordering(self):
        """Test todos are ordered by created_at (newest first)."""
        todo1 = Todo.objects.create(title='First', user=self.user)
        todo2 = Todo.objects.create(title='Second', user=self.user)
        
        todos = Todo.objects.all()
        self.assertEqual(todos[0], todo2)
        self.assertEqual(todos[1], todo1)


class CategoryModelTests(TestCase):
    """Test cases for Category model."""
    
    def test_create_category(self):
        """Test creating a category."""
        category = Category.objects.create(
            name='Personal',
            description='Personal tasks'
        )
        self.assertEqual(category.name, 'Personal')
        self.assertEqual(category.description, 'Personal tasks')
    
    def test_category_str_representation(self):
        """Test category string representation."""
        category = Category.objects.create(name='Shopping')
        self.assertEqual(str(category), 'Shopping')


class TodoViewTests(TestCase):
    """Test cases for todo views."""
    
    def setUp(self):
        """Set up test data and client."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Work',
            description='Work tasks'
        )
        self.todo = Todo.objects.create(
            title='Test Todo',
            description='Test Description',
            user=self.user,
            category=self.category
        )
    
    def test_todo_list_requires_login(self):
        """Test that todo list requires login."""
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_todo_list_view_logged_in(self):
        """Test todo list view when logged in."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.todo, response.context['todos'])
    
    def test_todo_list_shows_only_user_todos(self):
        """Test that users only see their own todos."""
        other_todo = Todo.objects.create(
            title='Other Todo',
            user=self.other_user
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('todo_list'))
        
        self.assertIn(self.todo, response.context['todos'])
        self.assertNotIn(other_todo, response.context['todos'])
    
    def test_create_todo_get(self):
        """Test GET request to create todo form."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('create_todo'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
    
    def test_create_todo_post(self):
        """Test POST request to create a new todo."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'New Todo',
            'description': 'New Description',
            'category': self.category.id,
            'completed': False
        }
        response = self.client.post(reverse('create_todo'), data)
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        new_todo = Todo.objects.get(title='New Todo')
        self.assertEqual(new_todo.user, self.user)
        self.assertEqual(new_todo.title, 'New Todo')
    
    def test_update_todo(self):
        """Test updating a todo."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Updated Todo',
            'description': 'Updated Description',
            'category': self.category.id,
            'completed': True
        }
        response = self.client.post(
            reverse('update_todo', args=[self.todo.id]),
            data
        )
        
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Todo')
        self.assertTrue(self.todo.completed)
    
    def test_update_other_user_todo_fails(self):
        """Test that users can't update other users' todos."""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(reverse('update_todo', args=[self.todo.id]))
        self.assertEqual(response.status_code, 404)
    
    def test_delete_todo(self):
        """Test deleting a todo."""
        self.client.login(username='testuser', password='testpass123')
        todo_id = self.todo.id
        response = self.client.post(reverse('delete_todo', args=[todo_id]))
        
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Todo.DoesNotExist):
            Todo.objects.get(id=todo_id)
    
    def test_toggle_todo_completion(self):
        """Test toggling todo completion status."""
        self.client.login(username='testuser', password='testpass123')
        
        self.assertFalse(self.todo.completed)
        
        self.client.post(reverse('toggle_todo', args=[self.todo.id]))
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.completed)
        
        self.client.post(reverse('toggle_todo', args=[self.todo.id]))
        self.todo.refresh_from_db()
        self.assertFalse(self.todo.completed)
    
    def test_filter_todos_by_category(self):
        """Test filtering todos by category."""
        other_category = Category.objects.create(name='Personal')
        todo2 = Todo.objects.create(
            title='Personal Todo',
            user=self.user,
            category=other_category
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('todo_list'),
            {'category': self.category.id}
        )
        
        self.assertIn(self.todo, response.context['todos'])
        self.assertNotIn(todo2, response.context['todos'])
    
    def test_filter_todos_by_status_pending(self):
        """Test filtering todos by pending status."""
        completed_todo = Todo.objects.create(
            title='Completed Todo',
            user=self.user,
            completed=True
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('todo_list'),
            {'status': 'pending'}
        )
        
        self.assertIn(self.todo, response.context['todos'])
        self.assertNotIn(completed_todo, response.context['todos'])
    
    def test_filter_todos_by_status_completed(self):
        """Test filtering todos by completed status."""
        completed_todo = Todo.objects.create(
            title='Completed Todo',
            user=self.user,
            completed=True
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('todo_list'),
            {'status': 'completed'}
        )
        
        self.assertNotIn(self.todo, response.context['todos'])
        self.assertIn(completed_todo, response.context['todos'])


class CategoryViewTests(TestCase):
    """Test cases for category views."""
    
    def setUp(self):
        """Set up test data and client."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Work',
            description='Work tasks'
        )
    
    def test_category_list_requires_login(self):
        """Test that category list requires login."""
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_category_list_view(self):
        """Test category list view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.category, response.context['categories'])
    
    def test_create_category(self):
        """Test creating a new category."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'name': 'Shopping',
            'description': 'Shopping tasks'
        }
        response = self.client.post(reverse('create_category'), data)
        
        self.assertEqual(response.status_code, 302)
        new_category = Category.objects.get(name='Shopping')
        self.assertEqual(new_category.description, 'Shopping tasks')
    
    def test_update_category(self):
        """Test updating a category."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'name': 'Updated Work',
            'description': 'Updated work tasks'
        }
        response = self.client.post(
            reverse('update_category', args=[self.category.id]),
            data
        )
        
        self.assertEqual(response.status_code, 302)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Work')
    
    def test_delete_category(self):
        """Test deleting a category."""
        self.client.login(username='testuser', password='testpass123')
        category_id = self.category.id
        response = self.client.post(reverse('delete_category', args=[category_id]))
        
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=category_id)


class FormValidationTests(TestCase):
    """Test cases for form validation."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
    
    def test_create_todo_without_title_fails(self):
        """Test that creating a todo without title fails."""
        data = {
            'title': '',
            'description': 'No title'
        }
        response = self.client.post(reverse('create_todo'), data)
        self.assertEqual(response.status_code, 200)  # Form re-rendered with errors
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
    
    def test_create_category_without_name_fails(self):
        """Test that creating a category without name fails."""
        data = {
            'name': '',
            'description': 'No name'
        }
        response = self.client.post(reverse('create_category'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)


class EdgeCaseTests(TestCase):
    """Test cases for edge cases."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_empty_todo_list(self):
        """Test todo list when no todos exist."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['todos']), 0)
    
    def test_empty_category_list(self):
        """Test category list when no categories exist."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['categories']), 0)
    
    def test_delete_category_with_assigned_todos(self):
        """Test deleting a category that has assigned todos."""
        category = Category.objects.create(name='Work')
        todo = Todo.objects.create(
            title='Task',
            user=self.user,
            category=category
        )
        
        self.client.login(username='testuser', password='testpass123')
        self.client.post(reverse('delete_category', args=[category.id]))
        
        todo.refresh_from_db()
        self.assertIsNone(todo.category)  # Category should be set to NULL
