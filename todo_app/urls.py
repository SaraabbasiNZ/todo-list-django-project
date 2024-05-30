from django.urls import path
from .views import home_view, todo_list_view, todo_item_create, edit_todo_item, delete_todo_item


app_name = 'todo_app'

urlpatterns = [
    path('', home_view, name='home'),
    path('list/', todo_list_view, name='todo_list'),
    path('create/', todo_item_create, name='todo_item_create'),
    path('<int:id>/edit/', edit_todo_item, name='todo_item_edit'),
    path('<id>/delete/', delete_todo_item, name='todo_item_delete'),
]