# Generated by Django 3.2.4 on 2022-07-24 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0047_studentmodel_refund_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodel',
            name='quarters_paid',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
