from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Todo

@csrf_exempt  # Add this decorator
def createTodo(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        todo = Todo.objects.create(**data)
        
        return JsonResponse({
            'message': 'Todo created successfully',
            'todo': {
                'id': todo.id,
                'title': todo.title,
                'description': todo.description
            }
        }, status=201)
    
    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def getTodos(request):
    if request.method == 'GET':
        todos = Todo.objects.filter(is_deleted=False)
        todo_list = [{
            'id': todo.id,
            'title': todo.title,
            'description': todo.description
        } for todo in todos]
        
        return JsonResponse({'todos': todo_list}, safe=False)

@csrf_exempt 
def updateTodo(request, pk): 
    if request.method == 'PUT':
        data = json.loads(request.body)
        todo = Todo.objects.get(pk=pk)
        todo.title = data.get('title', todo.title)
        todo.description = data.get('description', todo.description)
        todo.save()

        return JsonResponse({'message': 'Todo updated successfully'})
    return JsonResponse({'message': 'Method not allowed'}, status=405)

@csrf_exempt 
def deleteTodo(request, pk):
    if request.method == 'DELETE':
        todo = Todo.objects.get(pk=pk)
        todo.is_deleted = True
        todo.save()
        return JsonResponse({'message': 'Todo deleted successfully'})
    return JsonResponse({'message': 'Method not allowed'}, status=405)