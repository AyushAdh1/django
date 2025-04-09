from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.createTodo, name='create-todo'),
    path('list/', views.getTodos, name='get-todos'),
    path('update/<int:pk>/', views.updateTodo, name='update-todo'),
    path('delete/<int:pk>/', views.deleteTodo, name='delete-todo'),
]