from django.contrib import admin
from core.models import Funcionario, Camera, RegistroPostura, Usuario

class ModelAdminBase(admin.ModelAdmin):
    list_per_page = 20


@admin.register(Funcionario)
class FuncionarioAdmin(ModelAdminBase):
    list_display = (
        'id',
        'nome',
        'matricula',
        'cargo',
        'created_at',
    )


@admin.register(Camera)
class CameraAdmin(ModelAdminBase):
    list_display = (
        'id',
        'identificador',
        'funcionario',
        'created_at',
    )


@admin.register(RegistroPostura)
class RegistroPosturaAdmin(ModelAdminBase):
    list_display = (
        'id',
        'funcionario',
        'inicio',
        'fim',
        'duracao',
    )


@admin.register(Usuario)
class UsuarioAdmin(ModelAdminBase):
    list_display = (
        'id',
        'matricula',
        'funcionario',
        'is_active',
        'is_superuser',
        'is_staff',
        'last_login',
    )