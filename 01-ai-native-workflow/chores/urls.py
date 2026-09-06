from django.urls import path

from . import views

app_name = 'chores'

urlpatterns = [
    path('', views.index, name='index'),
    path('members/add/', views.member_create, name='member_create'),
    path('members/<int:pk>/edit/', views.member_edit, name='member_edit'),
    path('members/<int:pk>/delete/', views.member_delete, name='member_delete'),
    path('add/', views.chore_create, name='chore_create'),
    path('<int:pk>/edit/', views.chore_edit, name='chore_edit'),
    path('<int:pk>/delete/', views.chore_delete, name='chore_delete'),
    path('<int:pk>/complete/', views.chore_complete, name='chore_complete'),
]
