from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import FormView  
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Todo
from .forms import TodoForm
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer

@method_decorator(csrf_exempt, name='dispatch')
class TodoAPIView(APIView):
    permission_classes = [IsAuthenticated]  
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

@method_decorator(csrf_exempt, name='dispatch')
class TodoListView(APIView): 
    permission_classes = [IsAuthenticated]  # Add this line
    def get(self, request):
        todos = Todo.objects.filter(is_deleted=False)
        todo_list = [{
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'is_completed': todo.is_completed
        } for todo in todos]
        return Response(todo_list) 

@method_decorator(csrf_exempt, name='dispatch')
class TodoUpdateView(APIView):
    def put(self, request, pk):
        todo = Todo.objects.get(pk=pk)
        todo.title = request.data.get('title', todo.title)
        todo.description = request.data.get('description', todo.description)
        todo.is_completed = request.data.get('is_completed', todo.is_completed)
        todo.save()
        return Response({'message': 'Todo updated successfully'})

@method_decorator(csrf_exempt, name='dispatch')
class TodoDeleteView(View):
    def delete(self, request, pk):
        todo = Todo.objects.get(pk=pk)
        todo.is_deleted = True
        todo.save()
        return JsonResponse({'message': 'Todo deleted successfully'})

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