# Generated by Django 3.2.4 on 2022-08-07 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Agent', '0024_alter_agentmodel_gst_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agentmodel',
            name='commission',
        ),
        migrations.RemoveField(
            model_name='agentmodel',
            name='gst',
        ),
        migrations.RemoveField(
            model_name='agentmodel',
            name='gst_status',
        ),
    ]
