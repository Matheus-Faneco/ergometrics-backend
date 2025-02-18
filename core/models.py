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
    observacoes = models.CharField(
        db_column='tx_observacoes',
        max_length=256,
        null=True,
        blank = True,
        verbose_name="Observações"
    )
    total_alertas = models.IntegerField(
        db_column='nr_total_alertas',
        default=0,
        verbose_name="Total de Alertas"
    )
    duracao_segundos = models.IntegerField(
        db_column='nr_duracao_segundos',
        default=0,
        verbose_name="Duração em Segundos"
    )
    created_at = models.DateTimeField(
        db_column='dt_created',
        default=timezone.now,
        verbose_name="Data de criação"
    )

    def adicionar_alerta(self):
        self.total_alertas += 1
        self.save()

    #retornos de observacoes do funcionario
    def definir_observacoes(self):
        if self.duracao_segundos < 7200:
            return "Desempenho postural excelente."
        elif self.duracao_segundos < 14400:
            return "Desempenho postural aceitável."
        return "Alerta! Tempo excessivo em má postura."

    #salvando o return em observacoes
    def save(self, *args, **kwargs):
        self.observacoes = self.definir_observacoes()
        super().save(*args, **kwargs)

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


class RelatorioGeral(models.Model):
    total_alertas = models.IntegerField(
        db_column='nr_total_alertas',
        default=0,
        verbose_name="Total de Alertas"
    )
    media_alerta_por_funcionario = models.DecimalField(
        db_column='nr_media_alerta_por_funcionario',
        default=0.0,
        max_digits=5,
        decimal_places=2,
        verbose_name="Média de alerta por funcionário"
    )
    porcentagem_funcionario = models.DecimalField(
        db_column='nr_porcentagem_funcionario',
        default=0.0,
        max_digits=5,
        decimal_places=2,
        verbose_name="Porcentagem de alerta por funcionário"
    )

    class Meta:
        db_table = 'relatorio_geral'
        verbose_name = 'Relatório Geral'
        verbose_name_plural = 'Relatórios Gerais'


class UsuarioAdministrador(BaseUserManager):
    def create_user(self, password=None, **kwargs):
        funcionario = kwargs.pop('funcionario', None)

        if funcionario:
            matricula = funcionario.matricula
        else:
            matricula = kwargs.get('matricula')
            if not matricula:
                raise ValueError("Debe proveer matrícula o un funcionario válido")

        if 'matricula' in kwargs:
            kwargs.pop('matricula')

        user = self.model(
            matricula=matricula,
            funcionario=funcionario,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(password=password, **kwargs)


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