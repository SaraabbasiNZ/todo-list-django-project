from django import forms
from django.utils import timezone
from .models import TodoItem

class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['title', 'checked', 'date']

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date and date < timezone.now():
            raise forms.ValidationError("Please enter a date from today or future.")
        return date