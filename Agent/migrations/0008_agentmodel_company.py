# Generated by Django 3.2.4 on 2022-04-26 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agent', '0007_alter_agentmodel_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentmodel',
            name='company',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
