# Generated by Django 4.2.3 on 2023-08-04 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0005_expense_maintenance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='maintenance',
        ),
    ]
