# Generated by Django 3.1.4 on 2021-01-11 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantasy', '0003_tableteam_points'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameweek',
            name='match1',
        ),
        migrations.RemoveField(
            model_name='gameweek',
            name='match2',
        ),
        migrations.RemoveField(
            model_name='gameweek',
            name='match3',
        ),
        migrations.RemoveField(
            model_name='gameweek',
            name='match4',
        ),
        migrations.RemoveField(
            model_name='gameweek',
            name='match5',
        ),
        migrations.RemoveField(
            model_name='league',
            name='gameweek1',
        ),
        migrations.RemoveField(
            model_name='league',
            name='gameweek2',
        ),
        migrations.RemoveField(
            model_name='league',
            name='gameweek3',
        ),
        migrations.RemoveField(
            model_name='league',
            name='gameweek4',
        ),
        migrations.RemoveField(
            model_name='league',
            name='gameweek5',
        ),
        migrations.RemoveField(
            model_name='league',
            name='gameweek6',
        ),
        migrations.RemoveField(
            model_name='league',
            name='gameweek7',
        ),
        migrations.RemoveField(
            model_name='league',
            name='gameweek8',
        ),
        migrations.RemoveField(
            model_name='league',
            name='gameweek9',
        ),
        migrations.RemoveField(
            model_name='table',
            name='team1',
        ),
        migrations.RemoveField(
            model_name='table',
            name='team10',
        ),
        migrations.RemoveField(
            model_name='table',
            name='team2',
        ),
        migrations.RemoveField(
            model_name='table',
            name='team3',
        ),
        migrations.RemoveField(
            model_name='table',
            name='team4',
        ),
        migrations.RemoveField(
            model_name='table',
            name='team5',
        ),
        migrations.RemoveField(
            model_name='table',
            name='team6',
        ),
        migrations.RemoveField(
            model_name='table',
            name='team7',
        ),
        migrations.RemoveField(
            model_name='table',
            name='team8',
        ),
        migrations.RemoveField(
            model_name='table',
            name='team9',
        ),
        migrations.AddField(
            model_name='gameweek',
            name='matches',
            field=models.ManyToManyField(to='fantasy.Match'),
        ),
        migrations.AddField(
            model_name='league',
            name='gameweeks',
            field=models.ManyToManyField(to='fantasy.Gameweek'),
        ),
        migrations.AddField(
            model_name='table',
            name='teams',
            field=models.ManyToManyField(to='fantasy.TableTeam'),
        ),
    ]
