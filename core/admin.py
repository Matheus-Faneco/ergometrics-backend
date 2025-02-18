from django.contrib import admin
from core.models import Funcionario, Camera, Usuario

class ModelAdminBase(admin.ModelAdmin):
    list_per_page = 20

@admin.register(Funcionario)
class FuncionarioAdmin(ModelAdminBase):
    list_display = ("nome", "matricula", "cargo")
    search_fields = ("nome", "matricula")
    list_filter = ("cargo",)

@admin.register(Camera)
class CameraAdmin(ModelAdminBase):
    list_display = ("identificador", "funcionario")
    search_fields = ("identificador",)
    list_filter = ("funcionario",)


@admin.register(Usuario)
class UsuarioAdmin(ModelAdminBase):
    list_display = (
        "matricula", "funcionario", "ativo", "is_superuser", "is_staff")
    search_fields = ("matricula", "funcionario__nome")
    list_filter = ("ativo", "is_superuser", "is_staff")
