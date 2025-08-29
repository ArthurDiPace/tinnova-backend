"""
Modelos para o sistema de gestão de veículos.
"""
from django.db import models


class Marca(models.Model):
    """
    Modelo para armazenar marcas de veículos com validação de consistência.
    """
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Marca")
    ativo = models.BooleanField(default=True, verbose_name="Marca Ativa")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")


class Veiculo(models.Model):
    """
    Modelo para armazenar informações dos veículos seguindo a estrutura especificada.
    """
    veiculo = models.CharField(max_length=100, verbose_name="Nome do Veículo")
    marca = models.ForeignKey(
        Marca, 
        on_delete=models.PROTECT, 
        verbose_name="Marca",
        related_name='veiculos'
    )
    ano = models.IntegerField(verbose_name="Ano")
    cor = models.CharField(max_length=50, blank=True, verbose_name="Cor do Veículo")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    vendido = models.BooleanField(default=False, verbose_name="Vendido")
    excluido = models.BooleanField(default=False, verbose_name="Excluído")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def delete(self):
        self.excluido = True
        self.save()

