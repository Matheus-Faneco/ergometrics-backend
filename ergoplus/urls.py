from django.contrib import admin
from django.urls import path, include
from core import viewsets, views
from django.shortcuts import redirect

from rest_framework.routers import DefaultRouter

from core.views import LoginView, UsuarioView, LogoutView

router = DefaultRouter()
router.register(r'funcionarios', viewsets.FuncionarioViewSet)
router.register(r'camera', viewsets.CameraViewSet)
router.register(r'registro-postura', viewsets.RegistroPosturaViewSet)
router.register(r'usuario', viewsets.UsuarioViewSet)

#Maior parte das urls embaixo são devido a autenticação JWT
urlpatterns = [
    path('', lambda request: redirect('admin/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('login', LoginView.as_view()),
    path('usuario-auth', UsuarioView.as_view()),
    path('logout', LogoutView.as_view()),
]
