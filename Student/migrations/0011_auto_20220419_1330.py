# Generated by Django 3.1.3 on 2022-04-19 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0010_auto_20220419_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentmodel',
            name='application_fee',
            field=models.IntegerField(blank=True, default=250, null=True),
        ),
    ]
