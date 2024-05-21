from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo_app.urls')),
    path('accounts/', include('accounts.urls')),  # include the accounts URLs
]
