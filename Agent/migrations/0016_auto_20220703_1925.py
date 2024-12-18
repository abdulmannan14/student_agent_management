# Generated by Django 3.2.4 on 2022-07-03 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agent', '0015_auto_20220703_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentmodel',
            name='gst',
            field=models.IntegerField(blank=True, default=10, null=True),
        ),
        migrations.AlterField(
            model_name='agentmodel',
            name='gst_status',
            field=models.CharField(blank=True, choices=[('INCLUSIVE', 'INCLUSIVE'), ('EXCLUSIVE', 'EXCLUSIVE')], default='EXCLUSIVE', max_length=30, null=True),
        ),
    ]
