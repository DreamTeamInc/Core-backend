# Generated by Django 3.1.2 on 2020-10-24 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0007_auto_20201023_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
