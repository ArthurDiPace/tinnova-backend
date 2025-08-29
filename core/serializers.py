"""
Serializers para a API de veículos.
"""
from datetime import datetime
from rest_framework import serializers
from .models import Veiculo, Marca
from datetime import datetime


class MarcaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Marca."""
    
    MARCAS_VALIDAS = [
        'VOLKSWAGEN', 'FORD', 'CHEVROLET', 'FIAT', 'TOYOTA', 'HONDA', 
        'HYUNDAI', 'NISSAN', 'RENAULT', 'PEUGEOT', 'CITROEN', 'BMW',
        'MERCEDES-BENZ', 'AUDI', 'VOLVO', 'MAZDA', 'MITSUBISHI', 'SUBARU',
        'KIA', 'JEEP', 'DODGE', 'CHRYSLER', 'JAGUAR', 'LAND ROVER',
        'MINI', 'SMART', 'ALFA ROMEO', 'FERRARI', 'LAMBORGHINI', 'PORSCHE',
        'BENTLEY', 'ROLLS-ROYCE', 'ASTON MARTIN', 'MCLAREN', 'BUGATTI',
        'LOTUS', 'MASERATI', 'LEXUS', 'INFINITI', 'ACURA', 'GENESIS'
    ]
    
    class Meta:
        model = Marca
        fields = "__all__"
        read_only_fields = ['id', 'created', 'updated']
    
    def validate_nome(self, value):
        """
        Valida se o nome da marca está correto e consistente.
        Evita erros de digitação como 'Volksvagen', 'Forde', 'Xevrolé', etc.
        """
        nome_limpo = value.strip().upper()
        
        if nome_limpo not in self.MARCAS_VALIDAS:
            # Tenta encontrar marcas similares para sugestão
            marcas_similares = self._encontrar_marcas_similares(nome_limpo)
            
            if marcas_similares:
                raise serializers.ValidationError(
                    f"'{value}' não é uma marca válida. "
                    f"Possíveis marcas: {', '.join(marcas_similares)}"
                )
            else:
                raise serializers.ValidationError(
                    f"'{value}' não é uma marca válida. "
                    f"Verifique a grafia correta."
                )
        
        return nome_limpo
    
    def _encontrar_marcas_similares(self, nome_digitado):
        """
        Encontra marcas similares para sugestão em caso de erro de digitação.
        """
        nome_lower = nome_digitado.lower()
        marcas_similares = []
        
        for marca in self.MARCAS_VALIDAS:
            marca_lower = marca.lower()
            
            if nome_lower in marca_lower or marca_lower in nome_digitado:
                marcas_similares.append(marca)

            elif self._calcular_similaridade(nome_lower, marca_lower) > 0.5:
                marcas_similares.append(marca)

            elif nome_lower[:3] == marca_lower[:3]:
                marcas_similares.append(marca)

            elif self._caracteres_comuns(nome_lower, marca_lower) > 0.6:
                marcas_similares.append(marca)
        
        return marcas_similares[:3]
    
    def _calcular_similaridade(self, str1, str2):
        """
        Calcula similaridade simples entre duas strings.
        """
        if len(str1) < len(str2):
            str1, str2 = str2, str1
        
        if len(str2) == 0:
            return 0.0
        
        matches = sum(1 for a, b in zip(str1, str2) if a == b)
        return matches / len(str1)

    def _caracteres_comuns(self, str1, str2):
        """
        Calcula similaridade baseada em caracteres comuns.
        """
        if len(str1) < len(str2):
            str1, str2 = str2, str1
        
        if len(str2) == 0:
            return 0.0
        
        matches = 0
        for char in str2:
            if char in str1:
                matches += 1
        
        return matches / len(str2)


class VeiculoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Veiculo focado em validação de dados.
    """
    
    marca_nome = serializers.CharField(source='marca.nome', read_only=True)
    
    class Meta:
        model = Veiculo
        fields = "__all__"
        read_only_fields = ['id', 'created', 'updated']
        

    def to_representation(self, instance):
        """Customiza a representação do veículo."""
        representation = super().to_representation(instance)
        
        if representation.get('created'):
            representation['created'] = instance.created.strftime('%Y-%m-%d %H:%M:%S')
        
        if representation.get('updated'):
            representation['updated'] = instance.updated.strftime('%Y-%m-%d %H:%M:%S')
        
        return representation
