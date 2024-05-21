from django.shortcuts import render
from .models import TodoItem
from django.contrib.auth.decorators import login_required

# Create your views here.
def home_view(request):
    return render(request, 'todo_app/home.html')

@login_required(login_url='/accounts/login')
def todo_list_view(request):
    user = request.user
    query = TodoItem.objects.filter(owner = user)

    if request.method == 'POST':
        checked_list = request.POST.getlist('checked')
        checked_list = [int(i) for i in checked_list]
        for todo_item in query:
            if todo_item.id in checked_list:
                TodoItem.objects.filter(id = todo_item.id).update(checked=True)
            else:
                TodoItem.objects.filter(id = todo_item.id).update(checked=False)
        return redirect('/list')
        

    return render(request, 'todo_app/todo_list.html', {'todolist':query})
