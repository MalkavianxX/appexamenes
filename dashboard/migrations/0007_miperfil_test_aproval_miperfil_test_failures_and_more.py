# Generated by Django 4.1.7 on 2023-10-22 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_miexamen_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='miperfil',
            name='test_aproval',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='miperfil',
            name='test_failures',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='miperfil',
            name='test_incomplete',
            field=models.IntegerField(default=0),
        ),
    ]