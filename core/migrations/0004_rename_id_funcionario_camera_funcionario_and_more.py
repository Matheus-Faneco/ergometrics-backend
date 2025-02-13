# Generated by Django 5.1.6 on 2025-02-13 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_usuario_cs_staff_remove_usuario_cs_superuser_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='camera',
            old_name='id_funcionario',
            new_name='funcionario',
        ),
        migrations.RenameField(
            model_name='camera',
            old_name='tx_identificador',
            new_name='identificador',
        ),
        migrations.RenameField(
            model_name='funcionario',
            old_name='tx_cargo',
            new_name='cargo',
        ),
        migrations.RenameField(
            model_name='funcionario',
            old_name='tx_matricula',
            new_name='matricula',
        ),
        migrations.RenameField(
            model_name='funcionario',
            old_name='tx_nome',
            new_name='nome',
        ),
        migrations.RenameField(
            model_name='registropostura',
            old_name='dt_fim',
            new_name='fim',
        ),
        migrations.RenameField(
            model_name='registropostura',
            old_name='dt_inicio',
            new_name='inicio',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='cs_ativo',
            new_name='ativo',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='id_funcionario',
            new_name='funcionario',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='tx_matricula',
            new_name='matricula',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='tx_senha',
            new_name='senha',
        ),
    ]
