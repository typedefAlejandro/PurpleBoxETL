import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from sqlalchemy.orm import Session
from dbConfig import SessionLocal
from model.models import Usuario 

API_KEY = "69a70088782b7180fe4210c3f37b3bc9"  
LIMIT = 200


def buscar_amigos_do_usuario(username: str):
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getfriends&user={username}&limit={LIMIT}&api_key={API_KEY}&format=json"
    response = requests.get(url)

    if response.status_code != 200:
        print("Erro na requisição:", response.status_code)
        return []

    try:
        data = response.json()
        amigos = data["friends"]["user"]
        return [amigo["name"] for amigo in amigos]
    except KeyError:
        print("Usuário não possui amigos visíveis ou dados inválidos.")
        return []


def inserir_amigos_no_banco(amigos: list[str]):
    session: Session = SessionLocal()

    try:
        for nome in amigos:
            if not session.query(Usuario).filter_by(nome=nome).first():
                novo_usuario = Usuario(nome=nome)
                session.add(novo_usuario)

        session.commit()
        print(f"{len(amigos)} amigos inseridos com sucesso!")
    except Exception as e:
        session.rollback()
        print("Erro ao inserir usuários:", e)
    finally:
        session.close()


def main():
    usuario = input("Digite o nome do usuário Last.fm: ")
    amigos = buscar_amigos_do_usuario(usuario)

    if amigos:
        print(f"🔍 Amigos de {usuario}: {amigos}")
        inserir_amigos_no_banco(amigos)
    else:
        print("Nenhum amigo encontrado ou erro na consulta.")


if __name__ == "__main__":
    main()
