from rest_framework import viewsets, status
from rest_framework.response import Response
from .filters import FuncionarioFilter
from .models import Funcionario, Camera, Usuario, RelatorioGeral
from .serializers import FuncionarioSerializer, CameraSerializer, UsuarioSerializer, RelatorioGeralSerializer


class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    filterset_class = FuncionarioFilter
    ordering_fields = '__all__'
    ordering = '-id'

    def update(self, request, *args, **kwargs):
        # Incrementa o contador de alertas
        funcionario = self.get_object()
        funcionario.total_alertas += 1
        funcionario.save()

        # Retorna o funcionário atualizado
        serializer = self.get_serializer(funcionario)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RelatorioGeralViewSet(viewsets.ModelViewSet):
    queryset = RelatorioGeral.objects.all()
    serializer_class = RelatorioGeralSerializer
    ordering_fields = '__all__'
    ordering = '-id'

class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    ordering_fields = '__all__'
    ordering = '-id'


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    ordering_fields = '__all__'
    ordering = '-id'