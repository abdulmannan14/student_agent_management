# Generated by Django 4.2.16 on 2024-10-09 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0058_alter_studentmodel_gst_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodel',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='archived_tag',
            field=models.CharField(blank=True, choices=[('COMPLETED ARCHIVE', 'COMPLETED ARCHIVE'), ('WITHDRAWL ARCHIVE', 'WITHDRAWL ARCHIVE'), ('REFUNDED ARCHIVE', 'REFUNDED ARCHIVE')], max_length=50, null=True),
        ),
    ]