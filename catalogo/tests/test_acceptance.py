import pytest
from rest_framework import status
from model_bakery import baker
from catalogo.models import Avaliacao


@pytest.mark.django_db
def test_aceitacao_filtro_por_genero(api_client, genero):
    """
    Cenário 1 - Teste de Aceitação
    Filtro de Catálogo por Gênero (Baseado no CT03)
    """
    filme_acao = baker.make("catalogo.Filme", titulo="Filme de Ação Teste", ano=2023, sinopse="Teste")
    filme_acao.generos.add(genero)

    response = api_client.get(f"/api/filmes/filter/?genero={genero.id}")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1

    # Verificação mais robusta do gênero
    generos_encontrados = []
    for filme in response.data:
        if 'generos' in filme and isinstance(filme['generos'], list):
            generos_encontrados.extend([g.get('nome') for g in filme['generos'] if isinstance(g, dict)])

    assert genero.nome in generos_encontrados, f"Gênero '{genero.nome}' não encontrado na resposta"
    print("Teste de Aceitação - Filtro por Gênero: PASSED")


@pytest.mark.django_db
def test_aceitacao_fluxo_avaliacao_completo(authenticated_client, filme):
    """
    Cenário 2 - Teste de Aceitação
    Fluxo Completo de Avaliação (Baseado no TI02)
    """
    client, user = authenticated_client

    data = {
        "filme": filme.id,
        "nota": 5,
        "comentario": "Excelente filme! Recomendo fortemente."
    }

    response = client.post("/api/avaliacoes/", data, format="json")
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["nota"] == 5
    assert response.data["comentario"] == data["comentario"]

    # Verifica persistência
    avaliacao = Avaliacao.objects.get(usuario=user, filme=filme)
    assert avaliacao.nota == 5
    assert avaliacao.comentario == data["comentario"]

    print("Teste de Aceitação - Fluxo Completo de Avaliação: PASSED")


@pytest.mark.django_db
def test_regressao_email_unico(api_client):
    """
    Cenário 1 - Teste de Regressão
    Validação de E-mail Único (Pós-correção do TU01)
    """
    # Primeiro cadastro
    data1 = {
        "username": "usuario_teste1",
        "password": "SenhaForte123!",
        "password2": "SenhaForte123!",
        "email": "unico@teste.com"
    }
    response1 = api_client.post("/api/register/", data1, format="json")
    assert response1.status_code == status.HTTP_201_CREATED

    # Tentativa com e-mail duplicado
    data2 = {
        "username": "usuario_teste2",
        "password": "SenhaForte123!",
        "password2": "SenhaForte123!",
        "email": "unico@teste.com"
    }
    response2 = api_client.post("/api/register/", data2, format="json")
    
    # Mais flexível: aceita 400 ou 409
    assert response2.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT, 400, 409]
    
    error_msg = str(response2.data).lower()
    assert any(word in error_msg for word in ["email", "already", "duplicate", "exists", "único", "em uso"])

    print("Teste de Regressão - E-mail Único: PASSED")


@pytest.mark.django_db
def test_regressao_listagem_apos_avaliacao(authenticated_client, filme):
    """
    Cenário 2 - Teste de Regressão
    Atualização da Interface após Avaliação (Pós-correção do TI02)
    """
    client, _ = authenticated_client

    data = {"filme": filme.id, "nota": 4, "comentario": "Bom filme"}
    response = client.post("/api/avaliacoes/", data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    # Verifica se listagem continua funcionando
    response_list = client.get("/api/filmes/")
    assert response_list.status_code == status.HTTP_200_OK

    filme.refresh_from_db()
    assert filme.media_avaliacoes() > 0

    print("Teste de Regressão - Listagem após Avaliação: PASSED")
