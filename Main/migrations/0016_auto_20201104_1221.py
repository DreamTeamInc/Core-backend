# Generated by Django 3.1.2 on 2020-11-04 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0015_auto_20201103_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.BinaryField(),
        ),
    ]
