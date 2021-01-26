# Generated by Django 2.2.13 on 2021-01-05 21:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0003_task_order_squashed_0004_remove_task_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shared_tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]