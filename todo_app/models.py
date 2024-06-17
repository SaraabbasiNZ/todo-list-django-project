from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    PERSONAL = 'Personal'
    WORK = 'Work'
    STUDY = 'Study'
    HEALTH = 'Health'
    HOME = 'Home'
    OTHER = 'Other'

    CATEGORY_CHOICES = [
        (PERSONAL, 'Personal'),
        (WORK, 'Work'),
        (STUDY, 'Study'),
        (HEALTH, 'Health'),
        (HOME, 'Home'),
        (OTHER, 'Other'),
    ]

    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name


class Priority(models.Model):
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'

    PRIORITY_CHOICES = [
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    ]

    name = models.CharField(max_length=50, choices=PRIORITY_CHOICES)

    def __str__(self):
        return self.name


class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    checked = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title