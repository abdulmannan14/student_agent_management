# Generated by Django 3.2.4 on 2022-08-06 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0052_studentmodel_oshc_fee_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodel',
            name='refund_way',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
