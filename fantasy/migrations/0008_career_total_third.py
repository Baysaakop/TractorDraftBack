# Generated by Django 3.1.4 on 2021-01-25 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0007_auto_20210118_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='career',
            name='total_third',
            field=models.IntegerField(default=0),
        ),
    ]
