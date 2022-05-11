# Generated by Django 3.2.4 on 2022-04-18 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('country', models.CharField(blank=True, max_length=500, null=True)),
                ('phone', models.CharField(blank=True, max_length=500, null=True)),
                ('email', models.DateField(blank=True, null=True)),
            ],
        ),
    ]