# Generated by Django 4.1.7 on 2023-11-01 06:57

from django.db import migrations, models
import login.models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_alter_user_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='icon',
            field=models.ImageField(blank=True, default='profile_icons/avatar_def.png', null=True, upload_to='profile_icons', validators=[login.models.validate_file_type]),
        ),
    ]
