# Generated by Django 3.2.4 on 2022-04-26 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0031_studentmodel_amount_already_inserted'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodel',
            name='amount_inserting_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentmodel',
            name='amount_already_inserted',
            field=models.BooleanField(default=False),
        ),
    ]
