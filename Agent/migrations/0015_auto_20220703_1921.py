# Generated by Django 3.2.4 on 2022-07-03 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agent', '0014_alter_agentmodel_bonus'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentmodel',
            name='gst',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='agentmodel',
            name='gst_status',
            field=models.CharField(blank=True, choices=[('INCLUSIVE', 'INCLUSIVE'), ('EXCLUSIVE', 'EXCLUSIVE')], max_length=30, null=True),
        ),
    ]