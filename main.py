from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="VibeMusic API - Demo CI")


# Modelo de dados (Contrato de entrada/saída)
class Musica(BaseModel):
    titulo: str
    artista: str
    duracao: float


# Banco de dados em memória (Dicionário: ID -> Dados da Música)
db_musicas: dict[int, Musica] = {
    1: Musica(titulo="Bohemian Rhapsody",
              artista="Queen",
              duracao=5.9)
}


@app.get("/musicas/{musica_id}")
def buscar_musica(musica_id: int):
    if musica_id not in db_musicas:
        raise HTTPException(status_code=404,
                            detail="Música não encontrada")
    return db_musicas[musica_id]


@app.post("/musicas/{musica_id}", status_code=201)
def criar_musica(musica_id: int, musica: Musica):
    if musica.duracao <= 0:
        raise HTTPException(status_code=400,
                            detail="A duração deve ser maior que zero")
    if musica_id in db_musicas:
        raise HTTPException(status_code=400,
                            detail="ID já cadastrado")

    db_musicas[musica_id] = musica
    return {"mensagem": "Música cadastrada com sucesso",
            "musica": musica}


@app.put("/musicas/{musica_id}")
def atualizar_musica(musica_id: int,
                     musica: Musica):
    if musica_id not in db_musicas:
        raise HTTPException(status_code=404,
                            detail="Música não encontrada")
    if musica.duracao <= 0:
        raise HTTPException(status_code=400,
                            detail="A duração deve ser maior que zero")

    db_musicas[musica_id] = musica
    return {"mensagem": "Música atualizada",
            "musica": musica}


@app.delete("/musicas/{musica_id}")
def deletar_musica(musica_id: int):
    if musica_id not in db_musicas:
        raise HTTPException(status_code=404,
                            detail="Música não encontrada")

    del db_musicas[musica_id]
    return {"mensagem": "Música removida com sucesso"}


# Testando