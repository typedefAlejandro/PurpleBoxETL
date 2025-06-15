import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pycountry
from sqlalchemy.orm import Session
from dbConfig import SessionLocal
from model.models import Pais 

def popular_paises():
    session: Session = SessionLocal()

    try:
        for country in pycountry.countries:
            nome = country.name
            codigo = country.alpha_2 

            existe = session.query(Pais).filter_by(nome=nome).first()
            if not existe:
                novo_pais = Pais(nome=nome, codigo=codigo)
                session.add(novo_pais)

        session.commit()
        print("✅ Países inseridos com sucesso!")

    except Exception as e:
        session.rollback()
        print("❌ Erro ao inserir países:", e)

    finally:
        session.close()

if __name__ == "__main__":
    popular_paises()
