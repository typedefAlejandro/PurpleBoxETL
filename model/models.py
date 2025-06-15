from typing import List, Optional

from sqlalchemy import BigInteger, CheckConstraint, Column, DateTime, ForeignKeyConstraint, Index, Integer, PrimaryKeyConstraint, SmallInteger, String, Table, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Artista(Base):
    __tablename__ = 'artista'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='artista_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(255))
    ouvintes_globais: Mapped[Optional[int]] = mapped_column(BigInteger)
    playcount_globais: Mapped[Optional[int]] = mapped_column(BigInteger)

    artista_similar: Mapped[List['Artista']] = relationship('Artista', secondary='similaridade_artista', primaryjoin=lambda: Artista.id == t_similaridade_artista.c.artista_base_id, secondaryjoin=lambda: Artista.id == t_similaridade_artista.c.artista_similar_id, back_populates='artista_base')
    artista_base: Mapped[List['Artista']] = relationship('Artista', secondary='similaridade_artista', primaryjoin=lambda: Artista.id == t_similaridade_artista.c.artista_similar_id, secondaryjoin=lambda: Artista.id == t_similaridade_artista.c.artista_base_id, back_populates='artista_similar')
    album: Mapped[List['Album']] = relationship('Album', back_populates='artista')
    ranking_atual_artistas_paises: Mapped[List['RankingAtualArtistasPaises']] = relationship('RankingAtualArtistasPaises', back_populates='artista')
    musica: Mapped[List['Musica']] = relationship('Musica', back_populates='artista')
    tag: Mapped[List['Tag']] = relationship('Tag', secondary='artista_tag', back_populates='artista')


class Pais(Base):
    __tablename__ = 'pais'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pais_pkey'),
        UniqueConstraint('codigo', name='pais_codigo_key'),
        UniqueConstraint('nome', name='pais_nome_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    codigo: Mapped[Optional[str]] = mapped_column(String(3))

    ranking_atual_artistas_paises: Mapped[List['RankingAtualArtistasPaises']] = relationship('RankingAtualArtistasPaises', back_populates='pais')
    ranking_atual_musicas_paises: Mapped[List['RankingAtualMusicasPaises']] = relationship('RankingAtualMusicasPaises', back_populates='pais')


class Tag(Base):
    __tablename__ = 'tag'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='tag_pkey'),
        UniqueConstraint('nome', name='tag_nome_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))

    artista: Mapped[List['Artista']] = relationship('Artista', secondary='artista_tag', back_populates='tag')


class Usuario(Base):
    __tablename__ = 'usuario'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='usuario_pkey'),
        UniqueConstraint('nome', name='usuario_nome_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))


class Album(Base):
    __tablename__ = 'album'
    __table_args__ = (
        ForeignKeyConstraint(['artista_id'], ['artista.id'], ondelete='CASCADE', onupdate='CASCADE', name='album_artista_id_fkey'),
        PrimaryKeyConstraint('id', name='album_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(255))
    artista_id: Mapped[int] = mapped_column(Integer)
    playcount_globais: Mapped[Optional[int]] = mapped_column(BigInteger)

    artista: Mapped['Artista'] = relationship('Artista', back_populates='album')
    musica: Mapped[List['Musica']] = relationship('Musica', back_populates='album')


class RankingAtualArtistasPaises(Base):
    __tablename__ = 'ranking_atual_artistas_paises'
    __table_args__ = (
        ForeignKeyConstraint(['artista_id'], ['artista.id'], ondelete='CASCADE', onupdate='CASCADE', name='ranking_atual_artistas_paises_artista_id_fkey'),
        ForeignKeyConstraint(['pais_id'], ['pais.id'], ondelete='CASCADE', onupdate='CASCADE', name='ranking_atual_artistas_paises_pais_id_fkey'),
        PrimaryKeyConstraint('artista_id', 'pais_id', name='ranking_atual_artistas_paises_pkey'),
        Index('idx_raap_pais_posicao', 'pais_id', 'posicao_ranking')
    )

    artista_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pais_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    posicao_ranking: Mapped[int] = mapped_column(SmallInteger)
    data_ultima_atualizacao: Mapped[datetime.datetime] = mapped_column(DateTime)

    artista: Mapped['Artista'] = relationship('Artista', back_populates='ranking_atual_artistas_paises')
    pais: Mapped['Pais'] = relationship('Pais', back_populates='ranking_atual_artistas_paises')


t_similaridade_artista = Table(
    'similaridade_artista', Base.metadata,
    Column('artista_base_id', Integer, primary_key=True, nullable=False),
    Column('artista_similar_id', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['artista_base_id'], ['artista.id'], ondelete='CASCADE', onupdate='CASCADE', name='similaridade_artista_artista_base_id_fkey'),
    ForeignKeyConstraint(['artista_similar_id'], ['artista.id'], ondelete='CASCADE', onupdate='CASCADE', name='similaridade_artista_artista_similar_id_fkey'),
    PrimaryKeyConstraint('artista_base_id', 'artista_similar_id', name='similaridade_artista_pkey')
)


t_artista_tag = Table(
    'artista_tag', Base.metadata,
    Column('artista_id', Integer, primary_key=True, nullable=False),
    Column('tag_id', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['artista_id'], ['artista.id'], ondelete='CASCADE', onupdate='CASCADE'),
    ForeignKeyConstraint(['tag_id'], ['tag.id'], ondelete='CASCADE', onupdate='CASCADE'),
    PrimaryKeyConstraint('artista_id', 'tag_id')
)


class Musica(Base):
    __tablename__ = 'musica'
    __table_args__ = (
        ForeignKeyConstraint(['album_id'], ['album.id'], ondelete='CASCADE', onupdate='CASCADE', name='musica_album_id_fkey'),
        ForeignKeyConstraint(['artista_id'], ['artista.id'], ondelete='CASCADE', onupdate='CASCADE', name='musica_artista_id_fkey'),
        PrimaryKeyConstraint('id', name='musica_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(255))
    artista_id: Mapped[int] = mapped_column(Integer)
    duracao_faixa: Mapped[Optional[int]] = mapped_column(Integer)
    album_id: Mapped[Optional[int]] = mapped_column(Integer)

    album: Mapped[Optional['Album']] = relationship('Album', back_populates='musica')
    artista: Mapped['Artista'] = relationship('Artista', back_populates='musica')
    ranking_atual_musicas_paises: Mapped[List['RankingAtualMusicasPaises']] = relationship('RankingAtualMusicasPaises', back_populates='musica')


class RankingAtualMusicasPaises(Base):
    __tablename__ = 'ranking_atual_musicas_paises'
    __table_args__ = (
        ForeignKeyConstraint(['musica_id'], ['musica.id'], ondelete='CASCADE', onupdate='CASCADE', name='ranking_atual_musicas_paises_musica_id_fkey'),
        ForeignKeyConstraint(['pais_id'], ['pais.id'], ondelete='CASCADE', onupdate='CASCADE', name='ranking_atual_musicas_paises_pais_id_fkey'),
        PrimaryKeyConstraint('musica_id', 'pais_id', name='ranking_atual_musicas_paises_pkey'),
        Index('idx_ramp_pais_posicao', 'pais_id', 'posicao_ranking')
    )

    musica_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pais_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    posicao_ranking: Mapped[int] = mapped_column(SmallInteger)
    data_ultima_atualizacao: Mapped[datetime.datetime] = mapped_column(DateTime)

    musica: Mapped['Musica'] = relationship('Musica', back_populates='ranking_atual_musicas_paises')
    pais: Mapped['Pais'] = relationship('Pais', back_populates='ranking_atual_musicas_paises')
