import os, sys, time, requests
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert as pg_insert  

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dbConfig      import SessionLocal
from model.models  import Artista, Tag, t_artista_tag


API_KEY       = "d885f1790397b082118adbe7d96b6fde"   
WAIT_SECS     = 0.20                                 
HTTP_TIMEOUT  = 10                                   
CHECKPOINT_ID = 23281                                    

def fetch_tags(artist_name: str) -> list[str]:
    """Consulta Last.fm e devolve lista (sem duplicatas) de nomes de tags <= 100 chars."""
    time.sleep(WAIT_SECS)
    url = (
        "http://ws.audioscrobbler.com/2.0/"
        f"?method=artist.getinfo&artist={requests.utils.quote(artist_name)}"
        f"&api_key={API_KEY}&format=json"
    )
    try:
        r = requests.get(url, timeout=HTTP_TIMEOUT)
        if r.status_code != 200:
            print(f"⚠️  {artist_name}: HTTP {r.status_code}")
            return []
        raw = (
            r.json()
             .get("artist", {})
             .get("tags", {})
             .get("tag", [])
        )
        if isinstance(raw, dict):       
            raw = [raw]
        tags = {t["name"].strip()[:100].lower() for t in raw if t.get("name")}
        return list(tags)
    except Exception as exc:
        print(f"⚠️  {artist_name}: erro {exc}")
        return []

def main():
    sess: Session = SessionLocal()

    sub_has_tag = select(t_artista_tag.c.artista_id).distinct()

    artistas = (
        sess.query(Artista)
            .filter(~Artista.id.in_(sub_has_tag))        
            .filter(Artista.id >= CHECKPOINT_ID)         
            .order_by(Artista.id.asc())
            .all()
    )
    total = len(artistas)
    print(f"🎨  Artistas sem tags encontrados: {total} (a partir do ID {CHECKPOINT_ID})")

    for pos, art in enumerate(artistas, start=1):
        tag_names = fetch_tags(art.nome)
        if not tag_names:
            print(f"{pos}/{total:>6}  ℹ️  {art.nome}: sem tags")
            continue

        tag_ids = []
        for nome in tag_names:
            tag = sess.query(Tag).filter(func.lower(Tag.nome) == nome).first()
            if tag is None:
                tag = Tag(nome=nome)     
                sess.add(tag)
                sess.flush()            
            tag_ids.append(tag.id)

        novos = 0
        for tid in tag_ids:
            stmt = (
                pg_insert(t_artista_tag)
                .values(artista_id=art.id, tag_id=tid)
                .on_conflict_do_nothing()    
            )
            res = sess.execute(stmt)
            if res.rowcount:                 
                novos += 1

        sess.commit()
        print(f"{pos}/{total:>6}  ✅ {art.nome}: +{novos}/{len(tag_ids)} tag(s)")

    sess.close()
    print("🏁  Concluído.")

if __name__ == "__main__":
    main()
