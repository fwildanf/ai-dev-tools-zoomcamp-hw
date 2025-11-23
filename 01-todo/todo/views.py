from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Todo, Category
from .forms import TodoForm, CategoryForm


@login_required
def todo_list(request):
    """Display all todos for the logged-in user."""
    todos = Todo.objects.filter(user=request.user)
    categories = Category.objects.all()
    
    # Filter by category if provided
    category_id = request.GET.get('category')
    if category_id:
        todos = todos.filter(category_id=category_id)
    
    # Filter by completion status if provided
    status = request.GET.get('status')
    if status == 'completed':
        todos = todos.filter(completed=True)
    elif status == 'pending':
        todos = todos.filter(completed=False)
    
    context = {
        'todos': todos,
        'categories': categories,
        'selected_category': category_id,
        'selected_status': status,
    }
    return render(request, 'todo/home.html', context)


@login_required
def create_todo(request):
    """Create a new todo."""
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    
    return render(request, 'todo/todo_form.html', {'form': form, 'action': 'Create'})


@login_required
def update_todo(request, todo_id):
    """Update an existing todo."""
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    
    return render(request, 'todo/todo_form.html', {'form': form, 'action': 'Update', 'todo': todo})


@login_required
@require_http_methods(["POST"])
def delete_todo(request, todo_id):
    """Delete a todo."""
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()
    return redirect('todo_list')


@login_required
@require_http_methods(["POST"])
def toggle_todo(request, todo_id):
    """Toggle the completion status of a todo."""
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')


@login_required
def category_list(request):
    """Display all categories."""
    categories = Category.objects.all()
    return render(request, 'todo/category_list.html', {'categories': categories})


@login_required
def create_category(request):
    """Create a new category."""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'todo/category_form.html', {'form': form, 'action': 'Create'})


@login_required
def update_category(request, category_id):
    """Update an existing category."""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'todo/category_form.html', {'form': form, 'action': 'Update', 'category': category})


@login_required
@require_http_methods(["POST"])
def delete_category(request, category_id):
    """Delete a category."""
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('category_list')
