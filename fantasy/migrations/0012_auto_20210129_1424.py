# Generated by Django 3.1.4 on 2021-01-29 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0011_duel_league19_league19team'),
    ]

    operations = [
        migrations.AddField(
            model_name='career',
            name='total_appearance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='career',
            name='total_topscorer',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='career',
            name='total_vanga',
            field=models.IntegerField(default=0),
        ),
    ]
