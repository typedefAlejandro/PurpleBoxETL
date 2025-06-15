import sys
import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.orm import Session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dbConfig import SessionLocal
from model.models import Usuario, Artista

API_KEY = "199089dd72ee426b3fe65c5fe6418bd2"
LIMIT = 200
PAGE = 1

USERIDCHECKPOINT = 1345


def get_with_retry(url, retries=3, delay=2):
    for _ in range(retries):
        response = requests.get(url)
        if response.status_code == 429:
            print("⚠️ Rate limit atingido. Aguardando...")
            time.sleep(delay)
        else:
            return response
    return None


def get_top_artists(username):
    time.sleep(0.2) 
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={username}&page={PAGE}&limit={LIMIT}&api_key={API_KEY}&format=json"
    response = get_with_retry(url)
    if response is None or response.status_code != 200:
        print(f"❌ Falha ao buscar artistas de {username}")
        return []

    try:
        data = response.json()
        return [artist["name"] for artist in data["topartists"].get("artist", [])]
    except KeyError:
        print(f"⚠️ Nenhum artista encontrado para {username}")
        return []


def get_artist_info(artist_name):
    time.sleep(0.2)  # Delay para evitar limite
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist_name}&api_key={API_KEY}&format=json"
    response = get_with_retry(url)
    if response is None or response.status_code != 200:
        print(f"❌ Falha ao buscar info do artista {artist_name}")
        return None

    try:
        data = response.json()["artist"]
        nome = data["name"]
        ouvintes = int(data["stats"]["listeners"])
        playcount = int(data["stats"]["playcount"])
        return {"nome": nome, "ouvintes_globais": ouvintes, "playcount_globais": playcount}
    except (KeyError, ValueError):
        print(f"⚠️ Dados incompletos para artista {artist_name}")
        return None


def inserir_artistas(session: Session, artistas: list[dict]):
    count = 0
    for artista in artistas:
        if not session.query(Artista).filter_by(nome=artista["nome"]).first():
            novo_artista = Artista(
                nome=artista["nome"],
                ouvintes_globais=artista["ouvintes_globais"],
                playcount_globais=artista["playcount_globais"]
            )
            session.add(novo_artista)
            count += 1
    print(f"✅ Inseridos {count} novos artistas.")


def processar_usuario(username):
    session = SessionLocal()
    try:
        print(f"\n🎧 Buscando artistas de {username}...")
        nomes_artistas = get_top_artists(username)
        artistas_info = []

        for nome in nomes_artistas:
            info = get_artist_info(nome)
            if info:
                artistas_info.append(info)

        inserir_artistas(session, artistas_info)
        session.commit()

    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao processar {username}: {e}")
    finally:
        session.close()


def main():
    session = SessionLocal()
    try:
        usuarios = session.query(Usuario).filter(Usuario.id >= USERIDCHECKPOINT).all()
        nomes_usuarios = [u.nome for u in usuarios]
    finally:
        session.close()

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(processar_usuario, nomes_usuarios)


if __name__ == "__main__":
    main()
