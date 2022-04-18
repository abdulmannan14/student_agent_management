# Generated by Django 3.1.3 on 2022-03-28 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Restaurant', '0001_initial'),
        ('Order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TableModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.CharField(blank=True, max_length=500, null=True)),
                ('table_status', models.CharField(blank=True, choices=[('available', 'available'), ('occupied', 'occupied')], max_length=500, null=True)),
                ('order_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Order.ordermodel')),
                ('restaurant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Restaurant.restaurantmodel')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
