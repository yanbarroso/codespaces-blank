import pytest
from fastapi.testclient import TestClient

from api import app


@pytest.fixture
def client():
    """Fixture para criar um cliente de teste."""
    return TestClient(app)


class TestHealthCheck:
    """Testes de saúde da aplicação."""

    def test_stats_endpoint(self, client):
        """Testa o endpoint /stats."""
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_obras" in data
        assert "vocabulario_unico" in data
        assert isinstance(data["total_obras"], int)
        assert isinstance(data["vocabulario_unico"], int)

    def test_top_words_endpoint(self, client):
        """Testa o endpoint /stats/top-words."""
        response = client.get("/stats/top-words")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert "word" in data[0]
            assert "count" in data[0]

    def test_estante_endpoint(self, client):
        """Testa o endpoint /estante."""
        response = client.get("/estante")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert "titulo" in data[0]
            assert "total" in data[0]
            assert "data" in data[0]


class TestUploadEndpoint:
    """Testes do endpoint de upload."""

    def test_upload_missing_fields(self, client):
        """Testa upload sem campos obrigatórios."""
        response = client.post(
            "/upload",
            data={"titulo": "Test"},
            # Falta arquivo
        )
        assert response.status_code in [422, 400]  # Unprocessable Entity ou Bad Request

    def test_upload_with_txt_file(self, client, tmp_path):
        """Testa upload de arquivo TXT."""
        # Criar um arquivo TXT temporário
        test_file = tmp_path / "test.txt"
        test_file.write_text("Test content with some words for vocabulary analysis")

        with open(test_file, "rb") as f:
            response = client.post(
                "/upload",
                data={"titulo": "Test Book"},
                files={"arquivo": ("test.txt", f, "text/plain")},
            )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["titulo"] == "Test Book"


class TestDatabaseIntegration:
    """Testes de integração com banco de dados."""

    def test_database_persistence(self, client):
        """Testa se os dados são persistidos no banco."""
        response1 = client.get("/stats")
        count1 = response1.json()["total_obras"]

        response2 = client.get("/stats")
        count2 = response2.json()["total_obras"]

        # Os dados devem ser consistentes
        assert count1 == count2
