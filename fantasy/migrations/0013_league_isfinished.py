# Generated by Django 3.1.4 on 2021-02-07 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0012_auto_20210129_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='isFinished',
            field=models.BooleanField(default=False),
        ),
    ]
