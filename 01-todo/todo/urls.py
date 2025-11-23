from django.urls import path
from . import views

urlpatterns = [
    # Todo URLs
    path('', views.todo_list, name='todo_list'),
    path('create/', views.create_todo, name='create_todo'),
    path('<int:todo_id>/update/', views.update_todo, name='update_todo'),
    path('<int:todo_id>/delete/', views.delete_todo, name='delete_todo'),
    path('<int:todo_id>/toggle/', views.toggle_todo, name='toggle_todo'),
    
    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/<int:category_id>/update/', views.update_category, name='update_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
]
