# Generated by Django 3.1.3 on 2022-03-31 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Table', '0004_auto_20220329_1948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tablemodel',
            name='order_status',
        ),
        migrations.AlterField(
            model_name='tablemodel',
            name='table_status',
            field=models.CharField(blank=True, choices=[('available', 'available'), ('occupied', 'occupied')], default='available', max_length=500, null=True),
        ),
    ]
