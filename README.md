# Open-Critics CineReview(Guia de como iniciar o projeto e realiar os testes)

Sistema de avaliação de filmes com backend Django REST API e frontend estático em HTML/CSS/JS.

## Pré-requisitos

- Python 3.9+
- Git

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd Open-Critics
```

### 2. Criar e ativar o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows
```

### 3. Instalar dependências(com o virtual environment ativado)

```bash
pip install -r requirements.txt
```

### 4. Configurar o banco de dados

O projeto usa SQLite. As migrations criam as tabelas e populam o banco com gêneros e filmes de exemplo:

```bash
python manage.py migrate
```

### 5. Realizar os testes

Navegue até o diretório em que os testes estão inseridos e relize os testes
```bash
cd catalogo/tests
pytest test_*
```

## OPCIONAL ↓

### Iniciar o backend (API)

Em um terminal, com o ambiente virtual ativado:

```bash
python manage.py runserver 8001
```

A API ficará disponível em `http://localhost:8001/api/`.

### Iniciar o frontend

Em **outro terminal**:

```bash
cd frontend
python3 -m http.server 5500
```

O frontend ficará disponível em `http://localhost:5500/login.html`.

> **Importante:** o frontend deve ser acessado pela porta **5500**. A porta **8001** é exclusiva da API — abrir `http://localhost:8001/` no navegador retorna 404.

## URLs úteis


| Recurso      | URL                                                                        |
| ------------ | -------------------------------------------------------------------------- |
| Login        | [http://localhost:5500/login.html](http://localhost:5500/login.html)       |
| Cadastro     | [http://localhost:5500/register.html](http://localhost:5500/register.html) |
| API          | [http://localhost:8001/api/](http://localhost:8001/api/)                   |
| Admin Django | [http://localhost:8001/admin/](http://localhost:8001/admin/)               |


## Primeiro acesso

1. Acesse [http://localhost:5500/register.html](http://localhost:5500/register.html)
2. Crie uma conta (a senha deve ser forte, ex.: `MinhaSenha123!`)
3. Faça login em [http://localhost:5500/login.html](http://localhost:5500/login.html)

Para criar um superusuário e acessar o painel admin:

```bash
python manage.py createsuperuser
```

## Estrutura do projeto

```
Open-Critics/
├── catalogo/          # App Django (models, views, API)
├── filmes_project/    # Configurações do Django
├── frontend/          # Interface web (HTML, CSS, JS)
├── scripts/           # Scripts auxiliares (ex.: popular_banco.py)
└── manage.py
```

## Repopular o banco manualmente (opcional)

```bash
python scripts/popular_banco.py
```

