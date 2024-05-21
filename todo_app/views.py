from django.shortcuts import render
from .models import TodoItem

# Create your views here.
def home_view(request):
    return render(request, 'todo_app/home.html')
