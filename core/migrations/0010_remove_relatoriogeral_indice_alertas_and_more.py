# Generated by Django 5.1.6 on 2025-02-20 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_relatoriogeral_total_alertas_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relatoriogeral',
            name='indice_alertas',
        ),
        migrations.AddField(
            model_name='relatoriogeral',
            name='media_segundos_por_funcionario',
            field=models.DecimalField(db_column='nr_media_segundos_por_funcionario', decimal_places=2, default=0.0, max_digits=6, verbose_name='Média de segundos por funcionário'),
        ),
    ]
