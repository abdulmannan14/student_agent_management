# Generated by Django 3.1.3 on 2022-04-19 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0009_auto_20220419_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentmodel',
            name='agent_bonus',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]