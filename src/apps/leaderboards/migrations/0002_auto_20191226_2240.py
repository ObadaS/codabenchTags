# Generated by Django 2.1.11 on 2019-12-26 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboards', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='submissionscore',
            options={'ordering': ('column__index',)},
        ),
        migrations.AddField(
            model_name='column',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='column',
            name='computation',
            field=models.TextField(blank=True, choices=[('avg', 'Average'), ('sum', 'Sum'), ('min', 'Min'), ('max', 'Max')], null=True),
        ),
    ]