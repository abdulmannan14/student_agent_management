# Generated by Django 3.2.4 on 2022-07-20 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0043_alter_studentmodel_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodel',
            name='refunded',
            field=models.BooleanField(default=False),
        ),
    ]