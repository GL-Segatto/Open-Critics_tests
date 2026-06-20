import pytest
from rest_framework import status


@pytest.mark.django_db
class TestInterfacesAPI:

    # ==================== INTERFACE 1: FILMES ====================
    def test_listar_filmes_interface(self, api_client, filme):
        """
        Teste de Interface 1 - Listagem de Filmes
        """
        response = api_client.get("/api/filmes/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
        assert "titulo" in response.data[0]
        assert "media_avaliacoes" in response.data[0]

    def test_filme_trending_interface(self, api_client):
        """
        Teste de Interface 1 - Endpoint Trending
        """
        response = api_client.get("/api/filmes/trending/")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    # ==================== INTERFACE 2: AVALIAÇÕES ====================
    def test_criar_avaliacao_interface(self, authenticated_client, filme):
        """
        Teste de Interface 2 - Criar Avaliação
        """
        client, user = authenticated_client
        data = {
            "filme": filme.id,
            "nota": 5,
            "comentario": "Excelente filme! Muito bom."
        }
        response = client.post("/api/avaliacoes/", data, format="json")
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["nota"] == 5
        assert response.data.get("filme_titulo") == filme.titulo

    def test_listar_minhas_avaliacoes_interface(self, authenticated_client):
        """
        Teste de Interface 2 - Minhas Avaliações
        """
        client, _ = authenticated_client
        response = client.get("/api/avaliacoes/minhas/")
        assert response.status_code == status.HTTP_200_OK

    def test_avaliacao_sem_autenticacao(self, api_client, filme):
        """
        Teste de permissão - Avaliação sem autenticação
        """
        data = {"filme": filme.id, "nota": 4}
        response = api_client.post("/api/avaliacoes/", data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
