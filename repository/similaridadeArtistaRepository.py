import sys
import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from sqlalchemy.orm import Session
from sqlalchemy import insert, select

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dbConfig import SessionLocal
from model.models import Artista, t_similaridade_artista

API_KEY = "199089dd72ee426b3fe65c5fe6418bd2"
MAX_THREADS = 5


def get_similar_artist_name(artist_name):
    """Consulta a API e retorna o nome do primeiro artista similar."""
    time.sleep(0.2)
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist_name}&api_key={API_KEY}&format=json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        similares = data.get("artist", {}).get("similar", {}).get("artist", [])
        if similares:
            return similares[0]["name"]
    except Exception as e:
        print(f"⚠️ Erro ao buscar artista similar de {artist_name}: {e}")
    return None


def get_artist_info(artist_name):
    """Busca dados do artista via API e retorna um dicionário com nome, ouvintes e playcount."""
    time.sleep(0.2)
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist_name}&api_key={API_KEY}&format=json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json().get("artist", {})
        return {
            "nome": data["name"],
            "ouvintes_globais": int(data["stats"]["listeners"]),
            "playcount_globais": int(data["stats"]["playcount"]),
        }
    except Exception as e:
        print(f"⚠️ Falha ao obter dados de {artist_name}: {e}")
        return None


def processar_similaridade(artista):
    session: Session = SessionLocal()
    try:
        nome_similar = get_similar_artist_name(artista.nome)
        if not nome_similar:
            return f"⚠️ Nenhum artista similar para {artista.nome}"

        artista_similar = session.query(Artista).filter_by(nome=nome_similar).first()
        if not artista_similar:
            info = get_artist_info(nome_similar)
            if info:
                artista_similar = Artista(**info)
                session.add(artista_similar)
                session.commit()
                print(f"➕ Artista similar '{nome_similar}' inserido.")

        if not artista_similar:
            return f"⚠️ Não foi possível obter ou salvar '{nome_similar}'"

        if artista.id == artista_similar.id:
            return f"🚫 Ignorado: artista {artista.nome} similar a si mesmo."

        stmt = select(t_similaridade_artista).where(
            (t_similaridade_artista.c.artista_base_id == artista.id) &
            (t_similaridade_artista.c.artista_similar_id == artista_similar.id)
        )
        existe = session.execute(stmt).first()
        if existe:
            return f"ℹ️ Similaridade já existe: {artista.nome} → {nome_similar}"

        stmt_insert = insert(t_similaridade_artista).values(
            artista_base_id=artista.id,
            artista_similar_id=artista_similar.id
        )
        session.execute(stmt_insert)
        session.commit()
        return f"✅ Similaridade adicionada: {artista.nome} → {nome_similar}"

    except Exception as e:
        session.rollback()
        return f"❌ Erro com {artista.nome}: {e}"
    finally:
        session.close()


def main():
    session = SessionLocal()
    artistas = session.query(Artista).all()
    session.close()

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futuros = {executor.submit(processar_similaridade, artista): artista.nome for artista in artistas}
        for future in as_completed(futuros):
            print(future.result())


if __name__ == "__main__":
    main()
