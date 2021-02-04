# Generated by Django 3.1.4 on 2021-01-11 04:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import fantasy.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gameweek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('week', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gameweek_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=fantasy.models.item_directory_path)),
                ('total_champion', models.IntegerField(default=0)),
                ('total_runnerup', models.IntegerField(default=0)),
                ('total_point', models.IntegerField(default=0)),
                ('total_win', models.IntegerField(default=0)),
                ('total_draw', models.IntegerField(default=0)),
                ('total_loss', models.IntegerField(default=0)),
                ('total_score', models.IntegerField(default=0)),
                ('total_score_away', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manager_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manager_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_score', models.IntegerField(default=0)),
                ('away_score', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_team', to='fantasy.manager')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='match_created_by', to=settings.AUTH_USER_MODEL)),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='fantasy.manager')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='match_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=fantasy.models.item_directory_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='league_created_by', to=settings.AUTH_USER_MODEL)),
                ('gameweek1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gameweek1', to='fantasy.gameweek')),
                ('gameweek2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gameweek2', to='fantasy.gameweek')),
                ('gameweek3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gameweek3', to='fantasy.gameweek')),
                ('gameweek4', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gameweek4', to='fantasy.gameweek')),
                ('gameweek5', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gameweek5', to='fantasy.gameweek')),
                ('gameweek6', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gameweek6', to='fantasy.gameweek')),
                ('gameweek7', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gameweek7', to='fantasy.gameweek')),
                ('gameweek8', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gameweek8', to='fantasy.gameweek')),
                ('gameweek9', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gameweek9', to='fantasy.gameweek')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='league_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='gameweek',
            name='match1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match1', to='fantasy.match'),
        ),
        migrations.AddField(
            model_name='gameweek',
            name='match2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match2', to='fantasy.match'),
        ),
        migrations.AddField(
            model_name='gameweek',
            name='match3',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match3', to='fantasy.match'),
        ),
        migrations.AddField(
            model_name='gameweek',
            name='match4',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match4', to='fantasy.match'),
        ),
        migrations.AddField(
            model_name='gameweek',
            name='match5',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match5', to='fantasy.match'),
        ),
        migrations.AddField(
            model_name='gameweek',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gameweek_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
