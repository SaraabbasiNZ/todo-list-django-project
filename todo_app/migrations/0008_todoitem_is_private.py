# Generated by Django 4.2.13 on 2024-06-18 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0007_alter_priority_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='is_private',
            field=models.BooleanField(default=True),
        ),
    ]
