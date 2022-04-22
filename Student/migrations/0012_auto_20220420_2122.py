# Generated by Django 3.1.3 on 2022-04-20 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0011_auto_20220419_1330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentmodel',
            name='agent_commission',
        ),
        migrations.RemoveField(
            model_name='studentmodel',
            name='country',
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='course',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='paid_fee_fee',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='total_fee',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='warning_sent',
            field=models.BooleanField(default=False),
        ),
    ]
