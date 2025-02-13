# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone

class Funcionario(models.Model):
    nome = models.CharField(
        db_column='tx_nome',
        max_length=64,
        null=False,
        verbose_name="Nome"
    )
    matricula = models.CharField(
        db_column='tx_matricula',
        max_length=6,
        null=False,
        unique=True,
        verbose_name="Matrícula"
    )
    cargo = models.CharField(
        db_column='tx_cargo',
        max_length=64,
        null=False,
        verbose_name="Cargo"
    )
    created_at = models.DateTimeField(
        db_column='dt_created',
        default=timezone.now,
        verbose_name="Data de criação"
    )

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'funcionario'
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['nome']


class Usuario(AbstractUser, PermissionsMixin):
    funcionario = models.OneToOneField(
        Funcionario,
        on_delete=models.CASCADE,
        related_name='usuario',
        db_column='id_funcionario',
        verbose_name="Funcionário",
        null=True,
        blank=True,
    )
    matricula = models.CharField(
        db_column='tx_matricula',
        max_length=6,
        null=False,
        unique=True,
        verbose_name="Matrícula"
    )
    password = models.CharField(
        db_column='tx_password',
        max_length=128,
        verbose_name="Senha"
    )
    last_login = models.DateTimeField(
        db_column='dt_last_login',
        null=True,
        verbose_name="Último login"
    )
    is_active = models.BooleanField(
        db_column='cs_ativo',
        default=True,
        verbose_name="Ativo"
    )
    is_superuser = models.BooleanField(
        db_column='cs_superuser',
        default=False,
        verbose_name="Superusuário"
    )
    is_staff = models.BooleanField(
        db_column='cs_staff',
        default=False,
        verbose_name="Equipe"
    )
    username = models.CharField(
        max_length=150,
        default='',  # or any other default value
        unique=True,
        verbose_name="Username"
    )

    USERNAME_FIELD = 'matricula'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.matricula

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class Camera(models.Model):
    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cameras',
        db_column='id_funcionario',
        verbose_name="Funcionário"
    )
    identificador = models.CharField(
        db_column='tx_identificador',
        max_length=64,
        null=False,
        verbose_name="Identificador"
    )
    created_at = models.DateTimeField(
        db_column='dt_created',
        default=timezone.now,
        verbose_name="Data de criação"
    )

    def __str__(self):
        return f"Câmera {self.identificador}"

    class Meta:
        db_table = 'camera'
        verbose_name = 'Câmera'
        verbose_name_plural = 'Câmeras'


class RegistroPostura(models.Model):
    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.CASCADE,
        db_column='id_funcionario',
        verbose_name='Funcionário'
    )
    inicio = models.DateTimeField(
        db_column='dt_inicio',
        auto_now_add=True,
        verbose_name="Início da má postura"
    )
    fim = models.DateTimeField(
        db_column='dt_fim',
        null=True,
        blank=True,
        verbose_name="Fim da má postura"
    )
    duracao = models.IntegerField(
        db_column='nr_duracao',
        default=0,
        verbose_name="Duração (segundos)"
    )

    def save(self, *args, **kwargs):
        if self.fim and self.inicio:
            self.duracao = (self.fim - self.inicio).total_seconds()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.funcionario.nome} - {self.duracao}s"

    class Meta:
        db_table = 'registro_postura'
        verbose_name = 'Registro de Postura'
        verbose_name_plural = 'Registros de Postura'
        ordering = ['-inicio']