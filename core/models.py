from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

class Funcionario(models.Model):
    tx_nome = models.CharField(
        db_column='tx_nome',
        max_length=64,
        null=False,
        verbose_name="Nome"
    )
    tx_matricula = models.CharField(
        db_column='tx_matricula',
        max_length=6,
        null=False,
        unique=True,
        verbose_name="Matrícula"
    )
    tx_cargo = models.CharField(
        db_column='tx_cargo',
        max_length=64,
        null=False,
        verbose_name="Cargo"
    )

    def __str__(self):
        return self.tx_nome

    class Meta:
        db_table = 'funcionario'
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'


class Camera(models.Model):
    id_funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cameras',
        db_column='id_funcionario',
        verbose_name="Funcionário"
    )
    tx_identificador = models.CharField(
        db_column='tx_identificador',
        max_length=64,
        null=False,
        verbose_name="Identificador"
    )

    def __str__(self):
        return f"Câmera {self.tx_identificador} - {self.id_funcionario.tx_nome if self.id_funcionario else 'Sem funcionário'}"

    class Meta:
        db_table = 'camera'
        verbose_name = 'Câmera'
        verbose_name_plural = 'Câmeras'


class RegistroPostura(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    dt_inicio = models.DateTimeField(
        db_column='dt_inicio',
        null=True,
        blank=True,
        verbose_name="Início da má postura"
    )
    dt_fim = models.DateTimeField(
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
        if self.dt_fim and self.dt_inicio:
            self.duracao = (self.dt_fim - self.dt_inicio).total_seconds()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.funcionario.tx_nome} - {self.duracao} segundos"

    class Meta:
        db_table = 'registro_postura'
        verbose_name = 'Registro de Postura'
        verbose_name_plural = 'Registros de Postura'


class UsuarioAdministrador(BaseUserManager):
    def create_user(self, tx_matricula, password=None, id_funcionario=None):
        if not tx_matricula:
            raise ValueError("Matrícula inválida")

        user = self.model(tx_matricula=tx_matricula, id_funcionario=id_funcionario)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, tx_matricula, password=None, id_funcionario=None):
        user = self.create_user(tx_matricula, password, id_funcionario)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    id_funcionario = models.OneToOneField(
        Funcionario,
        on_delete=models.CASCADE,
        related_name='usuario',
        db_column='id_funcionario',
        verbose_name="Funcionário",
        null=True,
        blank=True,
    )
    tx_matricula = models.CharField(
        db_column='tx_matricula',
        max_length=6,
        null=False,
        unique=True,
        verbose_name="Matrícula"
    )
    tx_senha = models.CharField(
        db_column='tx_senha',
        max_length=64,
        null=False,
        verbose_name="Senha"
    )
    cs_ativo = models.BooleanField(
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

    USERNAME_FIELD = 'tx_matricula'

    def __str__(self):
        return self.tx_matricula

    def save(self, *args, **kwargs):
        if self.id_funcionario:
            self.tx_matricula = self.id_funcionario.tx_matricula
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
