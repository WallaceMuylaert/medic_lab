# Generated by Django 4.2.5 on 2023-10-05 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exames', '0002_alter_tiposexames_horario_final'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tiposexames',
            name='horario_final',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='tiposexames',
            name='horario_inicial',
            field=models.FloatField(),
        ),
    ]
