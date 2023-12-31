# Generated by Django 4.2.3 on 2023-08-22 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0010_car_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='file',
            field=models.FileField(default=1, upload_to='documents/files/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='document',
            name='picture',
            field=models.ImageField(upload_to='documents/images/'),
        ),
    ]
