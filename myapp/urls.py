from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('create/', views.TodoAPIView.as_view(), name='create-todo'),
    path('list/', views.TodoListView.as_view(), name='get-todos'),
    path('update/<int:pk>/', views.TodoUpdateView.as_view(), name='update-todo'),
    path('delete/<int:pk>/', views.TodoDeleteView.as_view(), name='delete-todo'),
    path('create-form/', views.TodoFormView.as_view(), name='create-todo-form'),
]