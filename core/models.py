from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
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
    total_alertas = models.IntegerField(
        db_column='nr_total_alertas',
        default=0,
        verbose_name="Total de Alertas"
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

    def __str__(self):
        return f"Câmera {self.identificador} - {self.funcionario.nome if self.funcionario else 'Sem funcionário'}"

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
        null=True,
        blank=True,
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
        return f"{self.funcionario.nome} - {self.duracao} segundos"

    class Meta:
        db_table = 'registro_postura'
        verbose_name = 'Registro de Postura'
        verbose_name_plural = 'Registros de Postura'
        ordering = ['-inicio']


class UsuarioAdministrador(BaseUserManager):
    def create_user(self, matricula, password=None, funcionario=None):
        if not matricula:
            raise ValueError("Matrícula inválida")

        user = self.model(matricula=matricula, funcionario=funcionario)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matricula, password=None, funcionario=None):
        user = self.create_user(matricula, password, funcionario)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
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
    senha = models.CharField(
        db_column='tx_senha',
        max_length=64,
        null=False,
        verbose_name="Senha"
    )
    ativo = models.BooleanField(
        db_column='cs_ativo',
        default=True,
        verbose_name="Ativo"
    )
    is_superuser = models.BooleanField(
        db_column='is_superuser',
        default=False,
        verbose_name="Superusuário"
    )
    is_staff = models.BooleanField(
        db_column='is_staff',
        default=False,
        verbose_name="Equipe"
    )

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    objects = UsuarioAdministrador()

    USERNAME_FIELD = 'matricula'

    def __str__(self):
        return self.matricula

    def save(self, *args, **kwargs):
        if self.funcionario:
            self.matricula = self.funcionario.matricula
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'