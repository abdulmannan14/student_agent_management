# Generated by Django 3.2.4 on 2022-07-04 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0040_paymodelstudent_is_tuition_and_material_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymodelstudent',
            name='agent_commision_amount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
