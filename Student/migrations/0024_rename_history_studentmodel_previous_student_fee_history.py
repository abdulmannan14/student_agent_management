# Generated by Django 3.2.4 on 2022-04-23 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0023_rename_previous_student_fee_history_studentmodel_history'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentmodel',
            old_name='history',
            new_name='previous_student_fee_history',
        ),
    ]
