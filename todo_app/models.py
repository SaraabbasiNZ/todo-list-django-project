from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from django.utils import timezone


HIGH = 'High'
MEDIUM = 'Medium'
LOW = 'Low'

PRIORITY_CHOICES = [
    (HIGH, 'High'),
    (MEDIUM, 'Medium'),
    (LOW, 'Low'),
]


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
    name = models.CharField(max_length=50, choices=PRIORITY_CHOICES)

    def __str__(self):
        return self.name


class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    checked = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )
    priority = models.ForeignKey(
        Priority,
        on_delete=models.SET_NULL,
        null=True
    )
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def is_public(self):
        return not self.is_private

    def save(self, *args, **kwargs):
        if self.date and self.date < timezone.now():
            raise ValidationError("The date cannot be in the past!")
        super(TodoItem, self).save(*args, **kwargs)
