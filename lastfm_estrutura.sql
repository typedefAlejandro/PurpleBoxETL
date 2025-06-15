--
-- PostgreSQL database dump
--

-- Dumped from database version 14.18 (Ubuntu 14.18-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.18 (Ubuntu 14.18-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: album; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.album (
    id integer NOT NULL,
    nome character varying(255) NOT NULL,
    playcount_globais bigint,
    artista_id integer NOT NULL
);


ALTER TABLE public.album OWNER TO postgres;

--
-- Name: album_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.album_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.album_id_seq OWNER TO postgres;

--
-- Name: album_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.album_id_seq OWNED BY public.album.id;


--
-- Name: artista; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.artista (
    id integer NOT NULL,
    nome character varying(255) NOT NULL,
    ouvintes_globais bigint,
    playcount_globais bigint
);


ALTER TABLE public.artista OWNER TO postgres;

--
-- Name: artista_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.artista_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.artista_id_seq OWNER TO postgres;

--
-- Name: artista_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.artista_id_seq OWNED BY public.artista.id;


--
-- Name: artista_tag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.artista_tag (
    artista_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.artista_tag OWNER TO postgres;

--
-- Name: musica; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.musica (
    id integer NOT NULL,
    nome character varying(255) NOT NULL,
    duracao_faixa integer,
    artista_id integer NOT NULL,
    album_id integer
);


ALTER TABLE public.musica OWNER TO postgres;

--
-- Name: musica_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.musica_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.musica_id_seq OWNER TO postgres;

--
-- Name: musica_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.musica_id_seq OWNED BY public.musica.id;


--
-- Name: pais; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pais (
    id integer NOT NULL,
    nome character varying(100) NOT NULL,
    codigo character varying(3)
);


ALTER TABLE public.pais OWNER TO postgres;

--
-- Name: pais_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pais_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pais_id_seq OWNER TO postgres;

--
-- Name: pais_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pais_id_seq OWNED BY public.pais.id;


--
-- Name: ranking_atual_artistas_paises; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ranking_atual_artistas_paises (
    artista_id integer NOT NULL,
    pais_id integer NOT NULL,
    posicao_ranking smallint NOT NULL,
    data_ultima_atualizacao timestamp without time zone NOT NULL
);


ALTER TABLE public.ranking_atual_artistas_paises OWNER TO postgres;

--
-- Name: ranking_atual_musicas_paises; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ranking_atual_musicas_paises (
    musica_id integer NOT NULL,
    pais_id integer NOT NULL,
    posicao_ranking smallint NOT NULL,
    data_ultima_atualizacao timestamp without time zone NOT NULL
);


ALTER TABLE public.ranking_atual_musicas_paises OWNER TO postgres;

--
-- Name: similaridade_artista; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.similaridade_artista (
    artista_base_id integer NOT NULL,
    artista_similar_id integer NOT NULL
);


ALTER TABLE public.similaridade_artista OWNER TO postgres;

--
-- Name: tag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tag (
    id integer NOT NULL,
    nome character varying(100) NOT NULL
);


ALTER TABLE public.tag OWNER TO postgres;

--
-- Name: tag_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tag_id_seq OWNER TO postgres;

--
-- Name: tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tag_id_seq OWNED BY public.tag.id;


--
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario (
    id integer NOT NULL,
    nome character varying(100) NOT NULL
);


ALTER TABLE public.usuario OWNER TO postgres;

--
-- Name: usuario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.usuario_id_seq OWNER TO postgres;

--
-- Name: usuario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuario_id_seq OWNED BY public.usuario.id;


--
-- Name: album id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.album ALTER COLUMN id SET DEFAULT nextval('public.album_id_seq'::regclass);


--
-- Name: artista id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artista ALTER COLUMN id SET DEFAULT nextval('public.artista_id_seq'::regclass);


--
-- Name: musica id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.musica ALTER COLUMN id SET DEFAULT nextval('public.musica_id_seq'::regclass);


--
-- Name: pais id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pais ALTER COLUMN id SET DEFAULT nextval('public.pais_id_seq'::regclass);


--
-- Name: tag id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tag ALTER COLUMN id SET DEFAULT nextval('public.tag_id_seq'::regclass);


--
-- Name: usuario id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id SET DEFAULT nextval('public.usuario_id_seq'::regclass);


--
-- Name: album album_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.album
    ADD CONSTRAINT album_pkey PRIMARY KEY (id);


--
-- Name: artista artista_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artista
    ADD CONSTRAINT artista_pkey PRIMARY KEY (id);


--
-- Name: artista_tag artista_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artista_tag
    ADD CONSTRAINT artista_tag_pkey PRIMARY KEY (artista_id, tag_id);


--
-- Name: musica musica_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.musica
    ADD CONSTRAINT musica_pkey PRIMARY KEY (id);


--
-- Name: pais pais_codigo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pais
    ADD CONSTRAINT pais_codigo_key UNIQUE (codigo);


--
-- Name: pais pais_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pais
    ADD CONSTRAINT pais_nome_key UNIQUE (nome);


--
-- Name: pais pais_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pais
    ADD CONSTRAINT pais_pkey PRIMARY KEY (id);


--
-- Name: ranking_atual_artistas_paises ranking_atual_artistas_paises_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ranking_atual_artistas_paises
    ADD CONSTRAINT ranking_atual_artistas_paises_pkey PRIMARY KEY (artista_id, pais_id);


--
-- Name: ranking_atual_musicas_paises ranking_atual_musicas_paises_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ranking_atual_musicas_paises
    ADD CONSTRAINT ranking_atual_musicas_paises_pkey PRIMARY KEY (musica_id, pais_id);


--
-- Name: similaridade_artista similaridade_artista_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.similaridade_artista
    ADD CONSTRAINT similaridade_artista_pkey PRIMARY KEY (artista_base_id, artista_similar_id);


--
-- Name: tag tag_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT tag_nome_key UNIQUE (nome);


--
-- Name: tag tag_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT tag_pkey PRIMARY KEY (id);


--
-- Name: usuario usuario_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_nome_key UNIQUE (nome);


--
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id);


--
-- Name: idx_album_artista; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_album_artista ON public.album USING btree (artista_id);


--
-- Name: idx_artista_nome_ci; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_artista_nome_ci ON public.artista USING btree (lower((nome)::text));


--
-- Name: idx_musica_album; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_musica_album ON public.musica USING btree (album_id);


--
-- Name: idx_musica_artista; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_musica_artista ON public.musica USING btree (artista_id);


--
-- Name: idx_pais_codigo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_pais_codigo ON public.pais USING btree (codigo);


--
-- Name: idx_pais_nome_ci; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_pais_nome_ci ON public.pais USING btree (lower((nome)::text));


--
-- Name: idx_raap_artista; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_raap_artista ON public.ranking_atual_artistas_paises USING btree (artista_id);


--
-- Name: idx_raap_pais_posicao; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_raap_pais_posicao ON public.ranking_atual_artistas_paises USING btree (pais_id, posicao_ranking);


--
-- Name: idx_ramp_musica; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ramp_musica ON public.ranking_atual_musicas_paises USING btree (musica_id);


--
-- Name: idx_ramp_pais_posicao; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ramp_pais_posicao ON public.ranking_atual_musicas_paises USING btree (pais_id, posicao_ranking);


--
-- Name: idx_similaridade_similar; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_similaridade_similar ON public.similaridade_artista USING btree (artista_similar_id);


--
-- Name: idx_tag_nome_ci; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_tag_nome_ci ON public.tag USING btree (lower((nome)::text));


--
-- Name: album album_artista_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.album
    ADD CONSTRAINT album_artista_id_fkey FOREIGN KEY (artista_id) REFERENCES public.artista(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: artista_tag artista_tag_artista_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artista_tag
    ADD CONSTRAINT artista_tag_artista_id_fkey FOREIGN KEY (artista_id) REFERENCES public.artista(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: artista_tag artista_tag_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artista_tag
    ADD CONSTRAINT artista_tag_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tag(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: musica musica_album_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.musica
    ADD CONSTRAINT musica_album_id_fkey FOREIGN KEY (album_id) REFERENCES public.album(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: musica musica_artista_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.musica
    ADD CONSTRAINT musica_artista_id_fkey FOREIGN KEY (artista_id) REFERENCES public.artista(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ranking_atual_artistas_paises ranking_atual_artistas_paises_artista_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ranking_atual_artistas_paises
    ADD CONSTRAINT ranking_atual_artistas_paises_artista_id_fkey FOREIGN KEY (artista_id) REFERENCES public.artista(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ranking_atual_artistas_paises ranking_atual_artistas_paises_pais_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ranking_atual_artistas_paises
    ADD CONSTRAINT ranking_atual_artistas_paises_pais_id_fkey FOREIGN KEY (pais_id) REFERENCES public.pais(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ranking_atual_musicas_paises ranking_atual_musicas_paises_musica_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ranking_atual_musicas_paises
    ADD CONSTRAINT ranking_atual_musicas_paises_musica_id_fkey FOREIGN KEY (musica_id) REFERENCES public.musica(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ranking_atual_musicas_paises ranking_atual_musicas_paises_pais_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ranking_atual_musicas_paises
    ADD CONSTRAINT ranking_atual_musicas_paises_pais_id_fkey FOREIGN KEY (pais_id) REFERENCES public.pais(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: similaridade_artista similaridade_artista_artista_base_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.similaridade_artista
    ADD CONSTRAINT similaridade_artista_artista_base_id_fkey FOREIGN KEY (artista_base_id) REFERENCES public.artista(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: similaridade_artista similaridade_artista_artista_similar_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.similaridade_artista
    ADD CONSTRAINT similaridade_artista_artista_similar_id_fkey FOREIGN KEY (artista_similar_id) REFERENCES public.artista(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

