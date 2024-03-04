# Generated by Django 5.0.2 on 2024-03-03 14:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets_checker', '0008_remove_ticket_vouchers'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='vouchers',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets_checker.partner', verbose_name='Vouchers'),
        ),
    ]
