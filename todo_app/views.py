from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import TodoItem, Category, Priority
from django.contrib.auth.decorators import login_required
from .forms import TodoItemForm
from django.core.exceptions import ValidationError
from django.contrib import messages


def home_view(request):
    todo_list = TodoItem.objects.filter(
        is_private=False
    ).order_by('priority', 'date')
    return render(request, 'todo_app/home.html', {'todolist': todo_list})


@login_required(login_url='/accounts/login')
def todo_list_view(request):
    user = request.user
    query = TodoItem.objects.filter(owner=user).order_by('priority', 'date')

    if request.method == 'POST':
        checked_list = request.POST.getlist('checked')
        checked_list = [int(i) for i in checked_list]
        for todo_item in query:
            if todo_item.id in checked_list:
                TodoItem.objects.filter(id=todo_item.id).update(checked=True)
            else:
                TodoItem.objects.filter(id=todo_item.id).update(checked=False)
        return redirect(reverse('todo_app:todo_list'))

    todo_list_len = len(query)
    return render(
        request, 'todo_app/todo_list.html', {
            'todolist': query, 'todo_list_len': todo_list_len
        }
    )


@login_required(login_url='/accounts/login')
def todo_item_create(request):
    user = request.user
    categories = Category.objects.all()
    priorities = Priority.objects.all()

    if request.method == 'POST':
        form = TodoItemForm(request.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.owner = user
                instance.save()
                messages.success(request, 'Task successfully created')
                return redirect('todo_app:todo_list')
            except ValidationError:
                messages.error(request, 'Task Date can not be in the past')
                form = TodoItemForm(request.POST)
                return render(
                    request, 'todo_app/create_todo_item.html', {
                        'form': form, 'categories': categories,
                        'priorities': priorities
                    }
                )
    else:
        form = TodoItemForm(categories=categories, priorities=priorities)
    return render(
        request, 'todo_app/create_todo_item.html', {
            'form': form, 'categories': categories,
            'priorities': priorities
        }
    )


@login_required(login_url='/accounts/login')
def edit_todo_item(request, id):
    todo_item = get_object_or_404(TodoItem, id=id, owner=request.user)
    categories = Category.objects.all()
    priorities = Priority.objects.all()

    if request.method == 'POST':
        form = TodoItemForm(request.POST, instance=todo_item)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Task successfully edited')
                return redirect('todo_app:todo_list')
            except ValidationError:
                messages.error(request, 'Task Date can not be in the past')
                form = TodoItemForm(request.POST, instance=todo_item)
                return render(
                    request, 'todo_app/edit_todo_item.html', {
                        'form': form, 'categories': categories,
                        'priorities': priorities
                    }
                )
    else:
        form = TodoItemForm(
            instance=todo_item, categories=categories,
            priorities=priorities)
    return render(
        request, 'todo_app/edit_todo_item.html', {
            'form': form, 'categories': categories, 'priorities': priorities
        }
    )


def delete_todo_item(request, id):
    item = get_object_or_404(TodoItem, id=id)
    if request.method == 'POST':
        if item.owner == request.user:
            item.delete()
            messages.success(request, 'Task successfully deleted')
            return redirect('todo_app:todo_list')
        else:
            return redirect('todo_app:todo_list')
    else:
        return render(request, 'todo_app/confirm_delete.html', {'item': item})
