# Generated by Django 2.0.5 on 2018-06-22 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_lesson_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]