# Generated by Django 3.2.4 on 2022-08-08 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0056_studentmodel_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymodelstudent',
            name='is_bonus',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
