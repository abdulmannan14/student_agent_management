# Generated by Django 3.2.4 on 2022-04-19 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0006_auto_20220419_0213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentmodel',
            name='commission',
            field=models.IntegerField(blank=True, default=30, null=True),
        ),
        migrations.AlterField(
            model_name='studentmodel',
            name='discount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentmodel',
            name='material_fee',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentmodel',
            name='non_refundable_fee',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentmodel',
            name='outstanding_fee',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentmodel',
            name='paid_fee',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentmodel',
            name='total_commission_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentmodel',
            name='total_required_fee',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentmodel',
            name='tuition_fee',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
