# Generated by Django 5.1.6 on 2025-02-13 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_salaryadvance_reason'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salaryadvance',
            name='repayment_start_date',
        ),
    ]
