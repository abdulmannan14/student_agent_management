# Generated by Django 3.2.4 on 2022-04-22 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0015_auto_20220422_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymodel',
            name='agent',
        ),
        migrations.AlterField(
            model_name='paymodel',
            name='paid_on',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
