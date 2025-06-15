import sys
import os
import time
import requests
from itertools import cycle
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.orm import Session
from sqlalchemy import desc

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dbConfig import SessionLocal
from model.models import Musica, Album, Artista

API_KEYS = [
    "d885f1790397b082118adbe7d96b6fde",
    "69a70088782b7180fe4210c3f37b3bc9",
    "199089dd72ee426b3fe65c5fe6418bd2",
    "23a6902acc27312840189085a12352a7"
]
api_key_iterator = cycle(API_KEYS)

CHECKPOINT_ALBUM_ID = 4432105
MAX_WORKERS = 16
DELAY_IF_ERROR = 1.0

def get_next_api_key():
    time.sleep(0.2) 
    return next(api_key_iterator)

def processar_album(album):
    session: Session = SessionLocal()
    try:
        artista = session.query(Artista).filter_by(id=album.artista_id).first()
        if not artista:
            print(f"⚠️ Artista com ID {album.artista_id} não encontrado.", flush=True)
            return

        api_key = get_next_api_key()
        url = f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={api_key}&artist={artista.nome}&album={album.nome}&format=json"

        print(f"🔍 Buscando faixas para: {album.nome} de {artista.nome}", flush=True)
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print(f"❌ Erro HTTP {response.status_code} para álbum '{album.nome}'", flush=True)
            time.sleep(DELAY_IF_ERROR)
            return

        try:
            data = response.json()
            faixas = data.get("album", {}).get("tracks", {}).get("track", [])
            if isinstance(faixas, dict):
                faixas = [faixas]

            novas = 0
            for faixa in faixas:
                nome = faixa.get("name")
                if not nome:
                    continue

                duracao = faixa.get("duration") or 130
                if session.query(Musica).filter_by(nome=nome, album_id=album.id).first():
                    continue

                nova_musica = Musica(
                    nome=nome,
                    duracao_faixa=int(duracao),
                    artista_id=artista.id,
                    album_id=album.id
                )
                session.add(nova_musica)
                novas += 1

            session.commit()
            print(f"✅ {novas} músicas inseridas do álbum '{album.nome}'", flush=True)

        except Exception as e:
            session.rollback()
            print(f"⚠️ Erro ao processar '{album.nome}': {e}", flush=True)

    finally:
        session.close()

def popular_musicas():
    session: Session = SessionLocal()
    try:
        albuns = session.query(Album).filter(Album.id >= CHECKPOINT_ALBUM_ID).all()
        print(f"🎵 Total de álbuns encontrados: {len(albuns)}", flush=True)
    finally:
        session.close()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(processar_album, albuns)

if __name__ == "__main__":
    popular_musicas()