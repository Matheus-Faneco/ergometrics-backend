from rest_framework import serializers
from .models import Funcionario, Camera, Usuario, RelatorioGeral


class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = '__all__'

class RelatorioGeralSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatorioGeral
        fields = '__all__'

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
