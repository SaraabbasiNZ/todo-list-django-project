from django.urls import path
from .views import home_view, todo_list_view, todo_item_create


app_name = 'todo_app'

urlpatterns = [
    path('', home_view, name='home'),
    path('list/', todo_list_view, name='todo_list'),
    path('create/', todo_item_create, name='todo_item_create'),
]