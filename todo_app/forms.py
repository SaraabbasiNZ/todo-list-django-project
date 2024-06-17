from django import forms
from django.utils import timezone
from .models import TodoItem, Category, Priority

class TodoItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    priority = forms.ModelChoiceField(queryset=Priority.objects.all(), required=False)
    
    class Meta:
        model = TodoItem
        fields = ['title', 'description', 'checked', 'date', 'category', 'priority']

    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories', None)
        priorities = kwargs.pop('priorities', None)
        super().__init__(*args, **kwargs)
        if categories:
            self.fields['category'].queryset = categories
        if priorities:
            self.fields['priority'].choices = priorities

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date and date < timezone.now():
            if not self.instance.pk:
                raise forms.ValidationError("Please enter a date from today or the future.")
        return date