# Generated by Django 5.1.6 on 2025-02-17 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='observacoes',
            field=models.CharField(db_column='tx_observacoes', max_length=256, null=True, verbose_name='Observações'),
        ),
    ]
