# Generated by Django 3.1.3 on 2022-04-20 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0012_auto_20220420_2122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentmodel',
            name='agent_bonus',
        ),
    ]
