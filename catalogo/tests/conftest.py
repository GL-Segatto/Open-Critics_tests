import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.fixture(autouse=True)
def enable_db_access(db):
    """Habilita acesso ao banco de dados em todos os testes"""
    pass


@pytest.fixture
def api_client():
    """Cliente API não autenticado"""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    """Cliente API autenticado + usuário"""
    user = baker.make(
        User, 
        username="testuser",
        email="testuser@test.com",
        first_name="Test",
        last_name="User"
    )
    user.set_password("testpass123")
    user.save()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def genero(db):
    """Fixture de Gênero"""
    return baker.make("catalogo.Genero", nome="Ação")


@pytest.fixture
def filme(db, genero):
    """Fixture de Filme com gênero"""
    filme = baker.make(
        "catalogo.Filme", 
        titulo="Filme Teste para Avaliação",
        sinopse="Sinopse de teste para os testes automatizados",
        ano=2023
    )
    filme.generos.add(genero)
    return filme
