# Generated by Django 3.2.4 on 2022-04-26 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Agent', '0008_agentmodel_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommissionModelAgent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_on', models.DateField(blank=True, null=True)),
                ('commission_left', models.IntegerField(blank=True, null=True)),
                ('agent_name', models.CharField(max_length=100, null=True)),
                ('agent_commission_percentage', models.CharField(max_length=100, null=True)),
                ('agent_commission_amount', models.CharField(max_length=100, null=True)),
                ('total_commission_paid', models.CharField(max_length=100, null=True)),
                ('student_paid_fee', models.CharField(max_length=100, null=True)),
                ('current_commission_amount', models.CharField(max_length=100, null=True)),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Agent.agentmodel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
