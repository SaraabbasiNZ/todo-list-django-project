from django.shortcuts import render, redirect, get_object_or_404
from .models import TodoItem
from django.contrib.auth.decorators import login_required
from .forms import TodoItemForm

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
    
    todo_list_len = len(query)
    return render(request, 'todo_app/todo_list.html', {'todolist': query,'todo_list_len': todo_list_len})


@login_required(login_url='/accounts/login')
def todo_item_create(request):
    user = request.user
    if request.method == 'POST':
        form = TodoItemForm(request.POST)
        if form.is_valid():
            instance = form.save(commit= False)
            instance.owner = user
            instance.save()
            return redirect('todo_app:todo_list')
    form = TodoItemForm()
    return render(request, 'todo_app/create_todo_item.html', {'form':form})


@login_required(login_url='/accounts/login')
def edit_todo_item(request, id):
    todo_item = get_object_or_404(TodoItem, id=id, owner=request.user)
    if request.method == 'POST':
        form = TodoItemForm(request.POST, instance=todo_item)
        if form.is_valid():
            form.save()
            return redirect('todo_app:todo_list')
    else:
        form = TodoItemForm(instance=todo_item)
    return render(request, 'todo_app/edit_todo_item.html', {'form': form})


def delete_todo_item(request, id):
    try:
        item = TodoItem.objects.get(id = id)
    except:
        return redirect('todo_app:todo_list')
    if item.owner == request.user:
        item.delete()
        return redirect('todo_app:todo_list')
    else:
        return redirect('todo_app:todo_list')