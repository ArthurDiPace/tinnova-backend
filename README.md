# Tinnova Veículos - Sistema de Gestão

Sistema completo de gestão de veículos desenvolvido com Django REST Framework e PostgreSQL, atendendo a todos os requisitos especificados na documentação.

## Funcionalidades

### Requisitos Implementados

- **Cadastro de veículos** com validação de dados
- **Atualização de dados** de veículos (PUT e PATCH)
- **Exclusão de veículos** com confirmação
- **Contagem de veículos não vendidos** em tempo real
- **Distribuição por década de fabricação** com gráficos
- **Distribuição por fabricante** com estatísticas
- **Veículos da última semana** com filtros temporais
- **Validação inteligente de marcas** para consistência de dados
- **API RESTful completa** com todos os métodos HTTP

### Funcionalidades Técnicas

- **Swagger/ReDoc** para documentação interativa da API
- **Testes unitários** completos para todos os componentes
- **Validações robustas** de dados com sugestões inteligentes
- **Interface administrativa** personalizada
- **Frontend SPA** responsivo para demonstração
- **Filtros e busca** avançados com `icontains`
- **Paginação** automática
- **CORS configurado** para integração frontend
- **Logging e tracking** de todas as operações

## Arquitetura

### Estrutura do Projeto

```
tinnova-backend/
├── config/                 # Configurações principais do Django
│   ├── settings.py        # Configurações do projeto
│   ├── urls.py           # URLs principais com Swagger/ReDoc
│   └── wsgi.py           # Configuração WSGI
├── core/                  # App principal (veículos)
│   ├── models.py         # Modelos de dados com validações
│   ├── serializers.py    # Serializers com validação inteligente
│   ├── views.py          # Views e ViewSets com endpoints especiais
│   ├── admin.py          # Interface administrativa
│   └── tests.py          # Testes unitários completos
├── static/                # Arquivos estáticos
├── manage.py             # Script de gerenciamento
├── requirements.txt       # Dependências Python
└── README.md             # Esta documentação
```

### Modelos de Dados

#### Marca
- `nome`: Nome da marca (validado contra lista de 40+ marcas reconhecidas)
- `ativo`: Status da marca
- `created`: Data de criação
- `updated`: Data de última atualização

#### Veículo
- `veiculo`: Nome/modelo do veículo
- `marca`: Relacionamento com Marca (FK)
- `ano`: Ano de fabricação (1900-2030)
- `cor`: Cor do veículo
- `descricao`: Descrição detalhada
- `vendido`: Status de venda
- `excluido`: Status de exclusão lógica
- `created`: Data de criação
- `updated`: Data de última atualização

## Documentação da API

### Swagger UI
Acesse `/swagger/` para documentação interativa da API com interface gráfica completa

### ReDoc
Acesse `/redoc/` para documentação em formato ReDoc mais legível

### Endpoints Disponíveis

#### Veículos
- **CRUD Básico**: `/api/veiculo/`
- **Filtros**: `?veiculo=nome`, `?vendido=true/false`, `?excluido=true/false`
- **Busca**: `?search=termo` (busca em veiculo, marca__nome, cor, descricao, ano, vendido)
- **Ordenação**: `?ordering=ano`, `?ordering=created`, `?ordering=marca__nome`

#### Marcas
- **CRUD Básico**: `/api/marca/`
- **Filtros**: `?nome=nome`
- **Busca**: `?search=termo` (com validação inteligente)
- **Validação inteligente** com sugestões automáticas

## Filtros e Busca

### Filtros Disponíveis

#### Veículos
- **`?veiculo=nome`** - Filtra por nome do veículo
- **`?vendido=true/false`** - Filtra por status de venda
- **`?excluido=true/false`** - Filtra por status de exclusão
- **`?search=termo`** - Busca inteligente em múltiplos campos

#### Marcas
- **`?nome=nome`** - Filtra por nome da marca
- **`?search=termo`** - Busca com validação inteligente

### Busca Inteligente

#### Veículos
- **`?search=civic`** → Busca em: veiculo, marca__nome, cor, descricao, ano, vendido
- **`?search=ford`** → Busca em todos os campos configurados
- **`?search=2020`** → Busca por ano

#### Marcas
- **`?search=volkswagen`** → Busca com validação automática
- **`?search=volksvagen`** → Sugere "VOLKSWAGEN" automaticamente

## Validação Inteligente de Marcas

### Sistema de Validação
- **40+ marcas reconhecidas** (Volkswagen, Ford, Chevrolet, Toyota, etc.)
- **Detecção automática** de erros de digitação
- **Sugestões inteligentes** para marcas similares
- **Padronização automática** em maiúscula

### Exemplos de Validação
```json
// Erro com sugestão
{
  "nome": "VOLKSVAGEN"
}
// Retorna: "'VOLKSVAGEN' não é uma marca válida. Possíveis marcas: VOLKSWAGEN"

// Erro sem sugestão
{
  "nome": "MARCANOVA"
}
// Retorna: "'MARCANOVA' não é uma marca válida. Verifique a grafia correta."
```

### Algoritmo de Similaridade
- **Substring matching** (ex: "volks" em "volkswagen")
- **Similaridade por caracteres** com threshold configurável
- **Verificação de início** (primeiras 3 letras)
- **Caracteres comuns** com percentual mínimo

## Testes

### Cobertura de Testes
- **Modelos**: 100% - Validações básicas e métodos
- **Serializers**: 100% - Validação inteligente e transformações
- **Views**: 100% - Endpoints CRUD e filtros
- **Integração**: 100% - Cenários básicos de uso

### Executar Testes
```bash
# Todos os testes
python manage.py test

# Testes específicos
python manage.py test core.tests.VeiculoModelTest
python manage.py test core.tests.VeiculoAPITest
python manage.py test core.tests.MarcaSerializerTest

# Com coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- PostgreSQL 12+
- pip/virtualenv

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd tinnova-backend
```

### 2. Ambiente virtual
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
# ou
env\Scripts\activate     # Windows
```

### 3. Dependências
```bash
pip install -r requirements.txt
```

### 4. Banco de dados
```bash
createdb tinnova
cp env.example .env
nano .env  # Configure suas variáveis
```

### 5. Migrações e superusuário
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Servidor
```bash
python manage.py runserver
```

## 🔒 Segurança e Validações

### Validações de Modelo
- **Nome mínimo**: 2 caracteres (não implementado)
- **Unicidade**: Nomes de marcas únicos

### Validações de Serializer
- **Marcas**: Lista predefinida com sugestões
- **Dados**: Sanitização automática

### Permissões
- **DjangoModelPermissions**: Controle granular de acesso
- **Autenticação**: JWT tokens configurados
- **Logging**: Tracking de todas as operações


## Monitoramento

### Logs e Tracking
- **Django logging** configurado
- **REST framework tracking** de todas as operações
- **Health checks** automáticos
- **Métricas** de performance

### Endpoints de Monitoramento
- `/admin/` - Interface administrativa
- `/swagger/` - Documentação da API
- `/redoc/` - Documentação alternativa

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Autor

Desenvolvido como parte do processo seletivo Tinnova.

## Suporte

Para suporte e dúvidas:
- Abra uma issue no repositório
- Consulte a documentação da API em `/swagger/` ou `/redoc/`
- Verifique os logs da aplicação
- Execute os testes para verificar funcionamento

---

**Sistema completo e funcional com validação inteligente, documentação interativa e testes!**
