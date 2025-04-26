from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.generic.edit import FormView  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication  # Add this import
from rest_framework.permissions import IsAuthenticated
from .models import Todo
from .forms import TodoForm
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer

class TodoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    
    def post(self, request):
        todo = Todo.objects.create(**request.data)
        return Response({
            'message': 'Todo created successfully',
            'todo': {
                'id': todo.id,
                'title': todo.title,
                'description': todo.description
            }
        }, status=201)

class TodoListView(APIView): 
    permission_classes = [IsAuthenticated],
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    
    def get(self, request):
        todos = Todo.objects.filter(is_deleted=False)
        todo_list = [{
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'is_completed': todo.is_completed
        } for todo in todos]
        return Response(todo_list) 

class TodoUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication,SessionAuthentication]
    
    def put(self, request, pk):
        todo = Todo.objects.get(pk=pk)
        todo.title = request.data.get('title', todo.title)
        todo.description = request.data.get('description', todo.description)
        todo.is_completed = request.data.get('is_completed', todo.is_completed)
        todo.save()
        return Response({'message': 'Todo updated successfully'})

class TodoDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication,SessionAuthentication]
    
    def delete(self, request, pk):
        todo = Todo.objects.get(pk=pk)
        todo.is_deleted = True
        todo.save()
        return Response({'message': 'Todo deleted successfully'})

class TodoFormView(FormView):
    template_name = 'todo_form.html'
    form_class = TodoForm

    def form_valid(self, form):
        todo = form.save()
        return JsonResponse({
            'message': 'Todo created successfully',
            'todo': {
                'id': todo.id,
                'title': todo.title,
                'description': todo.description
            }
        }, status=201)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})

class RegisterView(APIView):
    authentication_classes = [SessionAuthentication]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Registration successful',
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            })
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    authentication_classes = [SessionAuthentication]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            })
        return Response({'error': 'Invalid credentials'}, status=401)