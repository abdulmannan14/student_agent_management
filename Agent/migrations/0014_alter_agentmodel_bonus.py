# Generated by Django 3.2.4 on 2022-06-20 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agent', '0013_auto_20220430_0441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentmodel',
            name='bonus',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
