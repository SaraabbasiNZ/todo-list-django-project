# Generated by Django 4.2.13 on 2024-06-03 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0002_todoitem_date_todoitem_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
