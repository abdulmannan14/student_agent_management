# Generated by Django 3.2.4 on 2022-08-08 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0055_paymodelstudent_commission_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodel',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
