# Generated by Django 3.2.4 on 2022-07-04 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0041_paymodelstudent_agent_commision_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymodelstudent',
            name='agent_commision_amount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
