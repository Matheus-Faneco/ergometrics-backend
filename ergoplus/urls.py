from django.contrib import admin
from django.urls import path, include
from core import viewsets
from django.shortcuts import redirect

from rest_framework.routers import DefaultRouter

from core.viewsets import CameraViewSet, RegistroPosturaViewSet, UsuarioViewSet

router = DefaultRouter()
router.register(r'funcionarios', viewsets.FuncionarioViewSet)
router.register(r'cameras', CameraViewSet, basename='cameras')
router.register(r'registros-postura', RegistroPosturaViewSet, basename='registros-postura')
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
urlpatterns = [
    path('', lambda request: redirect('admin/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
