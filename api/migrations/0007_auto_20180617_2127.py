# Generated by Django 2.0.5 on 2018-06-17 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20180617_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='salt',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
