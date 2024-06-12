from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import TodoItem, Category
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
        return redirect(reverse('todo_app:todo_list'))
    
    todo_list_len = len(query)
    return render(request, 'todo_app/todo_list.html', {'todolist': query,'todo_list_len': todo_list_len})


@login_required(login_url='/accounts/login')
def todo_item_create(request):
    user = request.user
    categories = Category.objects.all()
    if request.method == 'POST':
        form = TodoItemForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = user
            instance.save()
            return redirect('todo_app:todo_list')
    else:
        form = TodoItemForm(categories=categories)    
    return render(request, 'todo_app/create_todo_item.html', {'form':form, 'categories': categories})


@login_required(login_url='/accounts/login')
def edit_todo_item(request, id):
    todo_item = get_object_or_404(TodoItem, id=id, owner=request.user)
    categories = Category.objects.all()
    if request.method == 'POST':
        form = TodoItemForm(request.POST, instance=todo_item)
        if form.is_valid():
            form.save()
            return redirect('todo_app:todo_list')
    else:
        form = TodoItemForm(instance=todo_item, categories=categories)    
    return render(request, 'todo_app/edit_todo_item.html', {'form': form, 'categories': categories})


def delete_todo_item(request, id):
    item = get_object_or_404(TodoItem, id=id)
    if request.method == 'POST':
        if item.owner == request.user:
            item.delete()
            return redirect('todo_app:todo_list')
        else:
            return redirect('todo_app:todo_list')
    else:
        return render(request, 'todo_app/confirm_delete.html', {'item': item})