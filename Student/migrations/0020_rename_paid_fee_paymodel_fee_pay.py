# Generated by Django 3.2.4 on 2022-04-23 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0019_studentmodel_quarterly_fee_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paymodel',
            old_name='paid_fee',
            new_name='fee_pay',
        ),
    ]
