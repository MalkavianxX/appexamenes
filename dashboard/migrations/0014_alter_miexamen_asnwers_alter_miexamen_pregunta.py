# Generated by Django 5.1.1 on 2024-10-14 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_reporte'),
        ('examenes', '0006_alter_respuesta_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miexamen',
            name='asnwers',
            field=models.ManyToManyField(to='examenes.respuesta'),
        ),
        migrations.AlterField(
            model_name='miexamen',
            name='pregunta',
            field=models.ManyToManyField(to='examenes.pregunta'),
        ),
    ]
