# Generated by Django 5.1.1 on 2024-09-19 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_invitation_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='miexamen',
            name='answers_response',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='miexamen',
            name='percent_time_ussles',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
