from django.db.models.aggregates import Sum
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from .filters import FuncionarioFilter
from .models import Funcionario, Camera, Usuario, RelatorioGeral
from .serializers import FuncionarioSerializer, CameraSerializer, UsuarioSerializer, RelatorioGeralSerializer


class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer

    # Modifique a função para buscar pelo campo matrícula
    @action(detail=True, methods=['patch'])
    def atualizar_por_matricula(self, request, matricula=None):
        try:
            funcionario = Funcionario.objects.get(matricula=matricula)
            serializer = self.get_serializer(funcionario, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Funcionario.DoesNotExist:
            return Response({"detail": "Funcionário não encontrado"}, status=status.HTTP_404_NOT_FOUND)



class RelatorioGeralViewSet(viewsets.ModelViewSet):
    queryset = RelatorioGeral.objects.all()
    serializer_class = RelatorioGeralSerializer
    ordering_fields = '__all__'
    ordering = '-id'

    @action(detail=False, methods=['post'])
    def atualizar_total_alertas(self, request):
        total_funcionarios = Funcionario.objects.all().count()

        total_alertas_funcionarios = Funcionario.objects.all().aggregate(Sum('total_alertas'))['total_alertas__sum'] or 0
        total_duracao_segundos = Funcionario.objects.aggregate(Sum('duracao_segundos'))['duracao_segundos__sum']


        media_alerta_por_funcionario = total_alertas_funcionarios / total_funcionarios
        media_segundos_por_funcionario = total_duracao_segundos / total_funcionarios

        relatorio, created = RelatorioGeral.objects.get_or_create(id=1)
        relatorio.total_alertas = total_alertas_funcionarios
        relatorio.media_segundos_por_funcionario = media_segundos_por_funcionario
        relatorio.media_alerta_por_funcionario = media_alerta_por_funcionario
        relatorio.save()

        ##teste no postman
        return Response({
            'total_alertas': relatorio.total_alertas,
            'media_alerta_por_funcionario': relatorio.media_alerta_por_funcionario,
            'media_segundos': relatorio.media_segundos_por_funcionario
        })


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    ordering_fields = '__all__'
    ordering = '-id'

    @action(detail=False, methods=['post'], url_path='atribuir-funcionario')
    def atribuir_funcionario(self, request):
        print("requisiçao recebida")
        matricula = request.data.get('matricula')
        print(f"requisiçao recebida: {matricula}")


        try:
            funcionario = Funcionario.objects.get(matricula=matricula)
        except Funcionario.DoesNotExist:
            return Response(
                {"detail": "Funcionário não foi encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        camera = self.get_queryset().first()
        if not camera:
            camera = Camera.objects.create()

        camera.funcionario = funcionario
        camera.save()

        return Response({"detail": "Funcionário atribuído"}, status=status.HTTP_200_OK)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    ordering_fields = '__all__'
    ordering = '-id'