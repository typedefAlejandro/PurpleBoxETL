# repository/tag_sequencial.py  – preenche tags a partir de um checkpoint
import os, sys, time, requests
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert as pg_insert   # ← p/ ON CONFLICT

# ---------------------------------------------------------------- caminhos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dbConfig      import SessionLocal
from model.models  import Artista, Tag, t_artista_tag

# ---------------------------------------------------------------- config
API_KEY       = "d885f1790397b082118adbe7d96b6fde"   # 1 (única) API‑key
WAIT_SECS     = 0.20                                 # pausa entre requests
HTTP_TIMEOUT  = 10                                   # timeout em segundos
CHECKPOINT_ID = 23281                                    # <<< mude aqui p/ recomeçar

# ---------------------------------------------------------------- helpers
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
        if isinstance(raw, dict):          # se vier somente 1 tag
            raw = [raw]
        # normaliza + corta p/ 100 caracteres (tamanho da coluna) e remove duplicados
        tags = {t["name"].strip()[:100].lower() for t in raw if t.get("name")}
        return list(tags)
    except Exception as exc:
        print(f"⚠️  {artist_name}: erro {exc}")
        return []

# ---------------------------------------------------------------- main
def main():
    sess: Session = SessionLocal()

    # sub‑consulta: quais artistas JÁ têm alguma tag
    sub_has_tag = select(t_artista_tag.c.artista_id).distinct()

    artistas = (
        sess.query(Artista)
            .filter(~Artista.id.in_(sub_has_tag))         # só quem ainda não tem tag
            .filter(Artista.id >= CHECKPOINT_ID)          # checkpoint
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

        # ---------- garante existência da tag e devolve lista de IDs ----------
        tag_ids = []
        for nome in tag_names:
            # busca case‑insensitive
            tag = sess.query(Tag).filter(func.lower(Tag.nome) == nome).first()
            if tag is None:
                tag = Tag(nome=nome)       # nome já está lower‑case & <= 100 chars
                sess.add(tag)
                sess.flush()               # gera tag.id sem commit
            tag_ids.append(tag.id)

        # ---------- associações artista <-> tag (ignora se já existir) ---------
        novos = 0
        for tid in tag_ids:
            stmt = (
                pg_insert(t_artista_tag)
                .values(artista_id=art.id, tag_id=tid)
                .on_conflict_do_nothing()      # não lança erro se já existir
            )
            res = sess.execute(stmt)
            if res.rowcount:                   # 1 linha inserida
                novos += 1

        sess.commit()
        print(f"{pos}/{total:>6}  ✅ {art.nome}: +{novos}/{len(tag_ids)} tag(s)")

    sess.close()
    print("🏁  Concluído.")

# -------------------------------------------------------------------------
if __name__ == "__main__":
    main()
