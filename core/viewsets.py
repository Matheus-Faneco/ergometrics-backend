from rest_framework import viewsets

from .filters import FuncionarioFilter
from .models import Funcionario, Camera, RegistroPostura, Usuario
from .serializers import FuncionarioSerializer, CameraSerializer, RegistroPosturaSerializer, UsuarioSerializer


class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    filterset_class = FuncionarioFilter
    ordering_fields = '__all__'
    ordering = '-id'

class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    ordering_fields = '__all__'
    ordering = '-id'

class RegistroPosturaViewSet(viewsets.ModelViewSet):
    queryset = RegistroPostura.objects.all()
    serializer_class = RegistroPosturaSerializer
    ordering_fields = '__all__'
    ordering = '-id'

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    ordering_fields = '__all__'
    ordering = '-id'