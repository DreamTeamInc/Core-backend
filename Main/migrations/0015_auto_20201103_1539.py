# Generated by Django 3.1.2 on 2020-11-03 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0014_auto_20201103_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mask',
            name='mask',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.BinaryField(editable=True),
        ),
    ]
