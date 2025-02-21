from django.contrib import admin
from django.urls import path, include
from core import viewsets, views
from django.shortcuts import redirect

from rest_framework.routers import DefaultRouter

from core.views import LoginView, UsuarioView, LogoutView, buscar_funcionario_por_matricula
from core.viewsets import FuncionarioViewSet

router = DefaultRouter()
router.register(r'funcionarios', viewsets.FuncionarioViewSet)
router.register(r'camera', viewsets.CameraViewSet)
router.register(r'usuario', viewsets.UsuarioViewSet)
router.register(r'relatorio-geral', viewsets.RelatorioGeralViewSet)

#Maior parte das urls embaixo são devido a autenticação JWT
class FuncionarioAlertasView:
    pass


urlpatterns = [
    path('', lambda request: redirect('admin/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('login', LoginView.as_view()),
    path('usuario-auth', UsuarioView.as_view()),
    path('logout', LogoutView.as_view()),
    path('api/funcionario/<str:matricula>/', buscar_funcionario_por_matricula, name='buscar-funcionario'),
    path('api/funcionarios/<str:id>/', path, name='atualizar_funcionario')



]
