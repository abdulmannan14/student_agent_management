# Generated by Django 3.2.4 on 2022-06-20 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0035_auto_20220510_0706'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymodelstudent',
            name='is_application_fee',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='paymodelstudent',
            name='is_material_fee',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
