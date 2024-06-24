from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from django.shortcuts import render


# Custom 404 handler function
def custom_404(request, exception):
    return render(request, '404.html', status=404)

# Register the custom 404 handler
handler404 = custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo_app.urls')),
    path('accounts/', include('accounts.urls')),
]
