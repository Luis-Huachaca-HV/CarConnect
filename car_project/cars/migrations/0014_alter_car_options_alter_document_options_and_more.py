# Generated by Django 4.2.3 on 2023-08-23 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0013_alter_expense_car'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='car',
            options={'verbose_name': 'Carro', 'verbose_name_plural': 'Carros'},
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'verbose_name': 'Documento', 'verbose_name_plural': 'Documentos'},
        ),
        migrations.AlterModelOptions(
            name='expense',
            options={'verbose_name': 'Gasto', 'verbose_name_plural': 'Gastos'},
        ),
        migrations.AlterModelOptions(
            name='expensetag',
            options={'verbose_name': 'Etiqueta de Gasto', 'verbose_name_plural': 'Etiquetas de Gastos'},
        ),
        migrations.AlterModelOptions(
            name='maintenance',
            options={'verbose_name': 'Mantenimiento', 'verbose_name_plural': 'Mantenimientos'},
        ),
    ]
