from django.urls import path
from django.shortcuts import redirect
from . import views

def redirect_to_todos(request):
    return redirect('create-todo-form')

urlpatterns = [
    path('', redirect_to_todos, name='home'),
    path('create/', views.createTodo, name='create-todo'),
    path('list/', views.getTodos, name='get-todos'), 
    path('update/<int:pk>/', views.updateTodo, name='update-todo'),
    path('delete/<int:pk>/', views.deleteTodo, name='delete-todo'),
    path('create-form/', views.createTodoForm, name='create-todo-form'),
]