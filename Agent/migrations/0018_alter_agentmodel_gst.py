# Generated by Django 3.2.4 on 2022-07-03 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agent', '0017_alter_agentmodel_gst'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentmodel',
            name='gst',
            field=models.CharField(blank=True, default=10, editable=False, max_length=10, null=True),
        ),
    ]
