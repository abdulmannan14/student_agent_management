# Generated by Django 3.2.4 on 2022-04-24 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0029_rename_paymodel_paymodelstudent'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodel',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
