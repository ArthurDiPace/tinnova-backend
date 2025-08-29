import logging

from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import viewsets, filters
from rest_framework_tracking.mixins import LoggingMixin

from .models import Veiculo, Marca
from .serializers import VeiculoSerializer, MarcaSerializer

logger = logging.getLogger(__name__)


class MarcaViewSet(LoggingMixin, viewsets.ModelViewSet):
    """
    ViewSet para gerenciar marcas de veículos.
    
    Permite operações CRUD completas em marcas, incluindo:
    - Listagem com filtros e paginação
    - Criação de novas marcas
    - Atualização de marcas existentes
    - Exclusão lógica (desativação)
    """
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nome']
    search_fields = ['nome']
    ordering_fields = ['nome', 'created_at']
    

class VeiculoViewSet(LoggingMixin, viewsets.ModelViewSet):
    """
    ViewSet para gerenciar veículos.
    
    Permite operações CRUD completas em veículos, incluindo:
    - Listagem com filtros avançados
    - Criação de novos veículos
    - Atualização completa e parcial
    - Exclusão com validação de negócio
    - Estatísticas e relatórios
    """
    queryset = Veiculo.objects.filter(excluido=False)
    serializer_class = VeiculoSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['veiculo', 'vendido', 'excluido']
    search_fields = ['veiculo', 'marca__nome', 'cor', 'descricao', 'ano', 'vendido']
    ordering_fields = ['ano', 'created', 'marca__nome', 'veiculo']

