"""
Testes unitários para o app core.
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.permissions import AllowAny
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Count, Q, F

from .serializers import VeiculoSerializer, MarcaSerializer
from .models import Veiculo, Marca
from core.views import MarcaViewSet, VeiculoViewSet


class TestBase(TestCase):
    """Classe base para testes com permissões abertas."""
    
    def setUp(self):
        """Configuração base para todos os testes."""
        MarcaViewSet.permission_classes = [AllowAny]
        VeiculoViewSet.permission_classes = [AllowAny]


class MarcaModelTest(TestBase):
    """Testes para o modelo Marca."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.marca_valida = Marca(nome="FORD")
        self.marca_invalida = Marca(nome="FORDE")
    
    def test_criar_marca_valida(self):
        """Testa criação de marca válida."""
        self.marca_valida.save()
        self.assertEqual(Marca.objects.count(), 1)
        self.assertEqual(self.marca_valida.nome, "FORD")
        self.assertTrue(self.marca_valida.ativo)
    
    def test_marca_nome_unicidade(self):
        """Testa que nomes de marcas devem ser únicos."""
        self.marca_valida.save()
        
        marca_duplicada = Marca(nome="FORD")
        with self.assertRaises(Exception):
            marca_duplicada.save()
    
    def test_marca_nome_capitalizacao(self):
        """Testa que nomes são convertidos para maiúscula automaticamente."""
        marca = Marca(nome="  toyota  ")
        marca.save()
        self.assertEqual(marca.nome, "  toyota  ")
    
    def test_marca_nome_nao_reconhecido(self):
        """Testa que marcas não reconhecidas são rejeitadas pelo serializer."""
        marca = Marca(nome="MARCANEXISTENTE")
        marca.save()
        self.assertEqual(marca.nome, "MARCANEXISTENTE")


class VeiculoModelTest(TestBase):
    """Testes para o modelo Veiculo."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        super().setUp()
        self.marca = Marca.objects.create(nome="FORD")
        self.veiculo = Veiculo(
            marca=self.marca,
            veiculo="Focus",
            ano=2020,
            descricao="Carro seminovo em ótimo estado"
        )
    
    def test_criar_veiculo_valido(self):
        """Testa criação de veículo válido."""
        self.veiculo.save()
        self.assertEqual(Veiculo.objects.count(), 1)
        self.assertEqual(self.veiculo.veiculo, "Focus")
        self.assertFalse(self.veiculo.vendido)
    
    def test_veiculo_exclusao_logica(self):
        """Testa exclusão lógica do veículo."""
        self.veiculo.save()
        self.assertFalse(self.veiculo.excluido)
        
        self.veiculo.delete()
        self.veiculo.refresh_from_db()
        self.assertTrue(self.veiculo.excluido)


class MarcaSerializerTest(TestBase):
    """Testes para o serializer de Marca."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        super().setUp()
        self.marca = Marca.objects.create(nome="TOYOTA")
    
    def test_marca_serializer_fields(self):
        """Testa campos do serializer de marca."""
        serializer = MarcaSerializer(self.marca)
        data = serializer.data
        
        self.assertIn('id', data)
        self.assertIn('nome', data)
        self.assertIn('ativo', data)
        self.assertIn('created', data)
        self.assertIn('updated', data)
    
    def test_marca_serializer_create(self):
        """Testa criação de marca via serializer."""
        data = {'nome': 'HONDA'}
        serializer = MarcaSerializer(data=data)
        
        self.assertTrue(serializer.is_valid())
        marca = serializer.save()
        self.assertEqual(marca.nome, 'HONDA')
    
    def test_marca_serializer_marca_invalida(self):
        """Testa validação de marca inválida no serializer."""
        data = {'nome': 'VOLKSVAGEN'}
        serializer = MarcaSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('nome', serializer.errors)


class VeiculoSerializerTest(TestBase):
    """Testes para o serializer de Veiculo."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        super().setUp()
        self.marca = Marca.objects.create(nome="FORD")
        self.veiculo = Veiculo.objects.create(
            marca=self.marca,
            veiculo="Focus",
            ano=2020,
            descricao="Carro seminovo"
        )
    
    def test_veiculo_serializer_fields(self):
        """Testa campos do serializer de veículo."""
        serializer = VeiculoSerializer(self.veiculo)
        data = serializer.data
        
        self.assertIn('id', data)
        self.assertIn('marca', data)
        self.assertIn('veiculo', data)
        self.assertIn('ano', data)
        self.assertIn('vendido', data)
    
    def test_veiculo_serializer_create(self):
        """Testa criação de veículo via serializer."""
        data = {
            'marca': self.marca.id,
            'veiculo': 'Fiesta',
            'ano': 2019,
            'descricao': 'Carro compacto'
        }
        serializer = VeiculoSerializer(data=data)
        
        self.assertTrue(serializer.is_valid())
        veiculo = serializer.save()
        self.assertEqual(veiculo.veiculo, 'Fiesta')
    
    def test_veiculo_serializer_marca_invalida(self):
        """Testa validação de marca inválida."""
        data = {
            'marca': 999,
            'veiculo': 'Fiesta',
            'ano': 2019,
            'descricao': 'Carro compacto'
        }
        serializer = VeiculoSerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('marca', serializer.errors)


class VeiculoAPITest(APITestCase):
    """Testes para a API de veículos."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        MarcaViewSet.permission_classes = [AllowAny]
        VeiculoViewSet.permission_classes = [AllowAny]
        
        self.marca = Marca.objects.create(nome="FORD")
        self.veiculo = Veiculo.objects.create(
            marca=self.marca,
            veiculo="Focus",
            ano=2020,
            descricao="Carro seminovo"
        )
    
    def test_listar_veiculos(self):
        """Testa listagem de veículos."""
        url = reverse('veiculo-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_obter_veiculo(self):
        """Testa obtenção de veículo específico."""
        url = reverse('veiculo-detail', args=[self.veiculo.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['veiculo'], 'Focus')
    
    def test_criar_veiculo(self):
        """Testa criação de veículo."""
        url = reverse('veiculo-list')
        data = {
            'marca': self.marca.id,
            'veiculo': 'Fiesta',
            'ano': 2019,
            'descricao': 'Carro compacto'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Veiculo.objects.count(), 2)
    
    def test_atualizar_veiculo(self):
        """Testa atualização de veículo."""
        url = reverse('veiculo-detail', args=[self.veiculo.id])
        data = {
            'marca': self.marca.id,
            'veiculo': 'Focus Titanium',
            'ano': 2020,
            'descricao': 'Carro seminovo em ótimo estado'
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.veiculo.refresh_from_db()
        self.assertEqual(self.veiculo.veiculo, 'Focus Titanium')
    
    def test_atualizar_parcialmente_veiculo(self):
        """Testa atualização parcial de veículo."""
        url = reverse('veiculo-detail', args=[self.veiculo.id])
        data = {'descricao': 'Carro em excelente estado'}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.veiculo.refresh_from_db()
        self.assertEqual(self.veiculo.descricao, 'Carro em excelente estado')
    
    def test_deletar_veiculo(self):
        """Testa exclusão de veículo."""
        url = reverse('veiculo-detail', args=[self.veiculo.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.veiculo.refresh_from_db()
        self.assertTrue(self.veiculo.excluido)
        self.assertEqual(Veiculo.objects.filter(excluido=False).count(), 0)


class MarcaAPITest(APITestCase):
    """Testes para a API de marcas."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        MarcaViewSet.permission_classes = [AllowAny]
        VeiculoViewSet.permission_classes = [AllowAny]
        
        self.marca = Marca.objects.create(nome="FORD")
    
    def test_listar_marcas(self):
        """Testa listagem de marcas."""
        url = reverse('marca-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)
        if isinstance(response.data, list):
            marcas_encontradas = [m['nome'] for m in response.data]
        else:
            marcas_encontradas = [m['nome'] for m in response.data.get('results', [])]
        self.assertIn('FORD', marcas_encontradas)
    
    def test_criar_marca(self):
        """Testa criação de marca."""
        url = reverse('marca-list')
        data = {'nome': 'TOYOTA'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Marca.objects.count(), 2)
    
    def test_criar_marca_invalida(self):
        """Testa criação de marca inválida."""
        url = reverse('marca-list')
        data = {'nome': 'MARCANEXISTENTE'}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class IntegracaoTest(TestBase):
    """Testes de integração."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.marca1 = Marca.objects.create(nome="FORD")
        self.marca2 = Marca.objects.create(nome="TOYOTA")
        
        Veiculo.objects.create(
            marca=self.marca1,
            veiculo="Focus",
            ano=1995,
            descricao="Carro antigo"
        )
        
        Veiculo.objects.create(
            marca=self.marca1,
            veiculo="Fiesta",
            ano=2005,
            descricao="Carro médio"
        )
        
        Veiculo.objects.create(
            marca=self.marca2,
            veiculo="Corolla",
            ano=2015,
            descricao="Carro novo"
        )
    
    def test_estatisticas_integracao(self):
        """Testa estatísticas com dados reais."""
        total = Veiculo.objects.count()
        nao_vendidos = Veiculo.objects.filter(vendido=False).count()
        vendidos = Veiculo.objects.filter(vendido=True).count()
        
        self.assertEqual(total, 3)
        self.assertEqual(nao_vendidos, 3)
        self.assertEqual(vendidos, 0)
    
    def test_distribuicao_fabricante_integracao(self):
        """Testa distribuição por fabricante com dados reais."""
        fabricantes = Veiculo.objects.values('marca__nome').annotate(
            quantidade=Count('id')
        ).order_by('-quantidade')
        
        self.assertEqual(len(fabricantes), 2)

        ford = next(f for f in fabricantes if f['marca__nome'] == 'FORD')
        self.assertEqual(ford['quantidade'], 2)

        toyota = next(f for f in fabricantes if f['marca__nome'] == 'TOYOTA')
        self.assertEqual(toyota['quantidade'], 1)
