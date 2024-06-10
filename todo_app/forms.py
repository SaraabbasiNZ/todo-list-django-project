from django import forms
from django.utils import timezone
from .models import TodoItem, Category

class TodoItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    
    class Meta:
        model = TodoItem
        fields = ['title', 'description', 'checked', 'date', 'category']

    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories', None)  # Get categories from kwargs
        super().__init__(*args, **kwargs)
        if categories:
            self.fields['category'].queryset = categories  # queryset for category field

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date and date < timezone.now():
            raise forms.ValidationError("Please enter a date from today or the future.")
        return date