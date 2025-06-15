import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.orm import Session


from dbConfig import SessionLocal
from model.models import Artista, Pais, RankingAtualArtistasPaises
from repository.artistaRepository import get_artist_info

API_KEY = "69a70088782b7180fe4210c3f37b3bc9"
LIMIT = 100

def get_with_retry(url, retries=3, delay=2):
    for _ in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 429:
                print("⚠️ Rate limit atingido. Aguardando...")
                time.sleep(delay)
            else:
                return response
        except requests.RequestException as e:
            print("Erro de conexão:", e)
            time.sleep(delay)
    return None

def buscar_top_artistas_por_pais(nome_pais):
    time.sleep(0.2)
    url = f"http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists&country={nome_pais}&limit={LIMIT}&api_key={API_KEY}&format=json"
    response = get_with_retry(url)
    if response is None or response.status_code != 200:
        print(f"❌ Falha ao buscar artistas para o país: {nome_pais}")
        return []
    try:
        data = response.json()
        return data["topartists"]["artist"]
    except KeyError:
        print(f"⚠️ Nenhum artista retornado para {nome_pais}")
        return []

def inserir_ranking_para_pais(session: Session, pais_id: int, artistas: list, nome_pais: str):
    count = 0
    for posicao, artista in enumerate(artistas, start=1):
        nome_artista = artista.get("name")
        if not nome_artista:
            continue

        artista_obj = session.query(Artista).filter_by(nome=nome_artista).first()
        if not artista_obj:
            info = get_artist_info(nome_artista)
            if info:
                artista_obj = Artista(
                    nome=info["nome"],
                    ouvintes_globais=info["ouvintes_globais"],
                    playcount_globais=info["playcount_globais"]
                )
                session.add(artista_obj)
                session.flush() 

        if artista_obj:
            ja_existe = session.query(RankingAtualArtistasPaises).filter_by(
                artista_id=artista_obj.id,
                pais_id=pais_id
            ).first()
            if ja_existe:
                continue

            ranking = RankingAtualArtistasPaises(
                artista_id=artista_obj.id,
                pais_id=pais_id,
                posicao_ranking=posicao,
                data_ultima_atualizacao=datetime.now()
            )
            session.add(ranking)
            count += 1

    print(f"✅ {count} registros inseridos para {nome_pais}")
    return count

def processar_pais(pais):
    session: Session = SessionLocal()
    try:
        artistas = buscar_top_artistas_por_pais(pais.nome)
        if artistas:
            inserir_ranking_para_pais(session, pais.id, artistas, pais.nome)
            session.commit()
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao processar país {pais.nome}: {e}")
    finally:
        session.close()

def main():
    session: Session = SessionLocal()
    try:
        paises = session.query(Pais).all()
    finally:
        session.close()

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(processar_pais, paises)

if __name__ == "__main__":
    main()
