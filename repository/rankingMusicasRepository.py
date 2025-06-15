import sys
import os
import time
import requests
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import cycle

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dbConfig import SessionLocal
from model.models import Artista, Album, Musica, Pais, RankingAtualMusicasPaises

API_KEYS = [
    "d885f1790397b082118adbe7d96b6fde",
    "69a70088782b7180fe4210c3f37b3bc9",
    "199089dd72ee426b3fe65c5fe6418bd2",
    "23a6902acc27312840189085a12352a7"
]
api_key_cycle = cycle(API_KEYS)

MAX_THREADS = 6
LIMIT = 100


def get_api_key():
    time.sleep(0.2)
    return next(api_key_cycle)

def processar_pais(pais):
    session = SessionLocal()
    try:
        api_key = get_api_key()
        url = f"http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country={pais.nome}&limit={LIMIT}&api_key={api_key}&format=json"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print(f"❌ Erro ao buscar músicas para {pais.nome}: {response.status_code}")
            return

        dados = response.json()
        tracks = dados.get("tracks", {}).get("track", [])
        if isinstance(tracks, dict):
            tracks = [tracks]

        for track in tracks:
            nome_musica = track.get("name")
            duracao = int(track.get("duration") or 130)
            ouvintes = int(track.get("listeners") or 0)
            artista_nome = track.get("artist", {}).get("name")
            rank = int(track.get("@attr", {}).get("rank", 0)) + 1

            if not nome_musica or not artista_nome:
                continue

            artista = session.query(Artista).filter_by(nome=artista_nome).first()
            if not artista:
                artista = Artista(nome=artista_nome, ouvintes_globais=ouvintes, playcount_globais=0)
                session.add(artista)
                session.flush()
                print(f"➕ Artista '{artista_nome}' inserido.")

            musica = session.query(Musica).filter_by(nome=nome_musica, artista_id=artista.id).first()
            if not musica:
                album = Album(nome=artista_nome, artista_id=artista.id, playcount_globais=ouvintes)
                session.add(album)
                session.flush()
                musica = Musica(
                    nome=nome_musica,
                    artista_id=artista.id,
                    album_id=album.id,
                    duracao_faixa=duracao
                )
                session.add(musica)
                session.flush()
                print(f"🎵 Música '{nome_musica}' inserida para artista '{artista_nome}'.")

            ja_existe = session.query(RankingAtualMusicasPaises).filter_by(musica_id=musica.id, pais_id=pais.id).first()
            if not ja_existe:
                ranking = RankingAtualMusicasPaises(
                    musica_id=musica.id,
                    pais_id=pais.id,
                    posicao_ranking=rank,
                    data_ultima_atualizacao=datetime.now()
                )
                session.add(ranking)

        session.commit()
        print(f"✅ Ranking de {pais.nome} inserido.")

    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao processar ranking de {pais.nome}: {e}")
    finally:
        session.close()

def main():
    session = SessionLocal()
    paises = session.query(Pais).all()
    session.close()

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futuros = [executor.submit(processar_pais, pais) for pais in paises]
        for future in as_completed(futuros):
            future.result()

if __name__ == "__main__":
    main()
