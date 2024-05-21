from django.urls import path
from .views import home_view, todo_list_view


app_name = 'todo_app'

urlpatterns = [
    path('', home_view, name='home'),
    path('list/', todo_list_view, name='todo_list')
]