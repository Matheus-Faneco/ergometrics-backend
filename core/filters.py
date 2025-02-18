import django_filters
from .models import Funcionario

class FuncionarioFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains')
    matricula = django_filters.CharFilter(lookup_expr='icontains')
    cargo = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Funcionario
        fields = ['nome', 'matricula', 'cargo']

