# Generated by Django 3.2.4 on 2022-08-02 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agent', '0022_alter_commissionmodelagent_mode_of_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentmodel',
            name='email2',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='agentmodel',
            name='email3',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]