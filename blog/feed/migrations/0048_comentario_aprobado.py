# Generated by Django 3.2.8 on 2021-12-11 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0047_notificaciones_nombre_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='aprobado',
            field=models.BooleanField(default=False),
        ),
    ]
