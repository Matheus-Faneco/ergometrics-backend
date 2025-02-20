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
    filterset_class = FuncionarioFilter
    ordering_fields = '__all__'
    ordering = '-id'


class RelatorioGeralViewSet(viewsets.ModelViewSet):
    queryset = RelatorioGeral.objects.all()
    serializer_class = RelatorioGeralSerializer
    ordering_fields = '__all__'
    ordering = '-id'

    @action(detail=False, methods=['post'])
    def atualizar_total_alertas(self, request):
        total_funcionarios = Funcionario.objects.all().count()

        total_alertas_funcionarios = Funcionario.objects.all().aggregate(Sum('total_alertas'))['total_alertas__sum'] or 0

        media_alerta_por_funcionario = total_alertas_funcionarios / total_funcionarios

        porcentagem_funcionario = (media_alerta_por_funcionario / total_alertas_funcionarios * 100)

        relatorio, created = RelatorioGeral.objects.get_or_create(id=1)
        relatorio.total_alertas = total_alertas_funcionarios
        relatorio.porcentagem_funcionario = porcentagem_funcionario
        relatorio.media_alerta_por_funcionario = media_alerta_por_funcionario
        relatorio.save()

        ##teste no postman
        return Response({
            'total_alertas': relatorio.total_alertas,
            'media_alerta_por_funcionario': relatorio.media_alerta_por_funcionario,
            'porcentagem_funcionario': relatorio.porcentagem_funcionario
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