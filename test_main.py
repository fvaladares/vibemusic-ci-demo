import pytest
from fastapi.testclient import TestClient
from main import app, db_musicas, Musica

client = TestClient(app)

# Fixture para resetar o banco em memória antes de CADA teste
@pytest.fixture(autouse=True)
def resetar_banco():
    db_musicas.clear()
    db_musicas[1] = Musica(titulo="Bohemian Rhapsody", artista="Queen", duracao=5.9)

def test_get_musica_existente():
    response = client.get("/musicas/1")
    assert response.status_code == 200
    assert response.json()["titulo"] == "Bohemian Rhapsody"

def test_post_criar_musica_valida():
    nova_musica = {"titulo": "Shape of You", "artista": "Ed Sheeran", "duracao": 3.9}
    response = client.post("/musicas/2", json=nova_musica)
    assert response.status_code == 201
    assert response.json()["musica"]["artista"] == "Ed Sheeran"

def test_post_bloquear_duracao_invalida():
    musica_invalida = {"titulo": "Erro", "artista": "Banda", "duracao": -2.0}
    response = client.post("/musicas/3", json=musica_invalida)
    assert response.status_code == 400
    assert response.json()["detail"] == "A duração deve ser maior que zero"

def test_put_atualizar_musica():
    musica_atualizada = {"titulo": "Bohemian Rhapsody (Remastered)", "artista": "Queen", "duracao": 6.0}
    response = client.put("/musicas/1", json=musica_atualizada)
    assert response.status_code == 200
    assert db_musicas[1].duracao == 6.0

def test_delete_remover_musica():
    response = client.delete("/musicas/1")
    assert response.status_code == 200
    assert 1 not in db_musicas