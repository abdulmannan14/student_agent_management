# Generated by Django 3.2.4 on 2022-04-24 03:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0028_alter_studentmodel_total_commission_paid'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PayModel',
            new_name='PayModelStudent',
        ),
    ]