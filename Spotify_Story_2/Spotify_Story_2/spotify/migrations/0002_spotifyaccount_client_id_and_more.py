# Generated by Django 5.1 on 2024-11-07 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='spotifyaccount',
            name='client_id',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='spotifyaccount',
            name='client_secret',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='spotifyaccount',
            name='spotify_id',
            field=models.CharField(max_length=50),
        ),
    ]