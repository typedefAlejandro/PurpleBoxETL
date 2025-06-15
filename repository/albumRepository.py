import sys
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from sqlalchemy.orm import Session
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dbConfig import SessionLocal
from model.models import Album, Artista


API_KEY = "69a70088782b7180fe4210c3f37b3bc9"
LIMIT = 100
MAX_THREADS = 5  
CHECKPOINT_INICIAL = 0
CHECKPOINT_FINAL = 90000000


def buscar_albuns_do_artista(nome_artista: str):
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={nome_artista}&limit={LIMIT}&api_key={API_KEY}&format=json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["topalbums"]["album"]
    except Exception as e:
        print(f"⚠️ Erro ao buscar álbuns de {nome_artista}: {e}")
        return []


def processar_artista(artista):
    session: Session = SessionLocal()
    inseridos = 0
    try:
        albuns = buscar_albuns_do_artista(artista.nome)
        for album in albuns:
            nome = album.get("name")
            playcount = album.get("playcount", 0)

            if not nome or session.query(Album).filter_by(nome=nome, artista_id=artista.id).first():
                continue

            novo_album = Album(
                nome=nome,
                playcount_globais=playcount,
                artista_id=artista.id
            )
            session.add(novo_album)
            inseridos += 1

        session.commit()
        return f"✅ {inseridos} álbuns inseridos para {artista.nome}"

    except Exception as e:
        session.rollback()
        return f"❌ Erro ao processar {artista.nome}: {e}"
    finally:
        session.close()


def inserir_albuns():
    session = SessionLocal()
    artistas = session.query(Artista).filter(Artista.id >= CHECKPOINT_INICIAL, Artista.id <= CHECKPOINT_FINAL).order_by(Artista.id).all()

    session.close()

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futuros = {executor.submit(processar_artista, artista): artista.nome for artista in artistas}
        for future in as_completed(futuros):
            print(future.result())


if __name__ == "__main__":
    inserir_albuns()
