# Generated by Django 3.1.4 on 2021-01-25 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0008_career_total_third'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameweek',
            name='matches',
            field=models.ManyToManyField(null=True, to='fantasy.Match'),
        ),
        migrations.AlterField(
            model_name='league',
            name='gameweeks',
            field=models.ManyToManyField(null=True, to='fantasy.Gameweek'),
        ),
        migrations.AlterField(
            model_name='manager',
            name='career',
            field=models.ManyToManyField(null=True, to='fantasy.Career'),
        ),
        migrations.AlterField(
            model_name='table',
            name='teams',
            field=models.ManyToManyField(null=True, to='fantasy.TableTeam'),
        ),
    ]
