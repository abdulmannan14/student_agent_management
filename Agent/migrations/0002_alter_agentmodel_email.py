# Generated by Django 3.2.4 on 2022-04-18 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agent', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentmodel',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]