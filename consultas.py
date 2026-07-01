# Dicionario de consultas 

CONSULTAS = {
    1: {
        "titulo": "Filmes de um gênero com nota média  [PARÂMETRO]",
        "descricao": "Título, gênero e nota média de todos os filmes de um gênero específico.",
        "parametros": [
            {"label": "Gênero (ex: Ficção Científica)", "tipo": "str"}
        ],
        "sql": """
            SELECT v.titulo, g.nome AS genero, v.nota_media
            FROM view_media_filmes v
            JOIN Filme_Genero fg ON v.id_filme = fg.id_filme
            JOIN Generos g ON fg.id_genero = g.id_genero
            WHERE g.nome = %s
        """
    },
    2: {
        "titulo": "Média das notas por gênero",
        "descricao": "Média das notas de avaliação agrupadas por gênero.",
        "sql": """
            SELECT g.nome AS genero, ROUND(AVG(v.nota_media), 2) AS media_do_genero
            FROM Generos g
            JOIN Filme_Genero fg USING(id_genero)
            JOIN view_media_filmes v USING(id_filme)
            GROUP BY g.nome
        """
    },
    3: {
        "titulo": "Séries favoritas de um usuário  [PARÂMETRO]",
        "descricao": "Séries que o usuário avaliou acima da sua própria média geral.",
        "parametros": [
            {"label": "Nome do usuário (ex: Bruno Costa)", "tipo": "str"}
        ],
        "sql": """
            SELECT u.nome, s.titulo, aseries.nota
            FROM AvaliacoesSeries aseries
            JOIN Usuarios u USING(id_usuario)
            JOIN Series s USING(id_serie)
            WHERE u.nome = %s AND aseries.nota > (
                SELECT AVG(todas_notas.nota)
                FROM (
                    SELECT id_usuario, nota FROM AvaliacoesSeries
                    UNION ALL
                    SELECT id_usuario, nota FROM AvaliacoesFilmes
                ) todas_notas
                WHERE todas_notas.id_usuario = aseries.id_usuario
            )
        """
    },
    4: {
        "titulo": "Profissionais que participaram de mais de 1 filme",
        "descricao": "Nome e total de filmes dos profissionais com mais de uma participação.",
        "sql": """
            SELECT p.nome AS profissional, COUNT(ef.id_filme) AS total_filmes
            FROM Profissionais p
            JOIN ElencoFilme ef USING(id_profissional)
            JOIN Filmes f USING(id_filme)
            GROUP BY p.nome
            HAVING COUNT(ef.id_filme) > 1
        """
    },
    5: {
        "titulo": "Usuários que avaliaram todos os filmes de uma saga  [PARÂMETRO]",
        "descricao": "Usuários que avaliaram todos os filmes de uma saga específica.",
        "parametros": [
            {"label": "Nome da saga (ex: O Senhor dos Anéis)", "tipo": "str"}
        ],
        "sql": """
            SELECT u.nome
            FROM Usuarios u
            WHERE NOT EXISTS (
                SELECT f.id_filme FROM Filmes f WHERE f.saga = %s
                EXCEPT
                SELECT af.id_filme FROM AvaliacoesFilmes af
                WHERE af.id_usuario = u.id_usuario
            )
        """
    },
    6: {
        "titulo": "Gêneros por número de filmes e duração média",
        "descricao": "Gêneros ordenados por quantidade de filmes, com duração média em minutos.",
        "sql": """
            SELECT g.nome AS nome_genero,
                   COUNT(fg.id_filme) AS total_filmes,
                   ROUND(AVG(f.duracao_segundos) / 60.0, 2) AS minutos
            FROM Generos g
            JOIN Filme_Genero fg ON g.id_genero = fg.id_genero
            JOIN Filmes f ON fg.id_filme = f.id_filme
            GROUP BY g.id_genero, g.nome
            ORDER BY total_filmes DESC
        """
    },
    7: {
        "titulo": "Atores em séries de Drama com episódios longos",
        "descricao": "Atores e personagens em séries de Drama com episódios acima de 50 minutos.",
        "sql": """
            SELECT DISTINCT p.nome AS ator, es.personagem, s.titulo AS serie
            FROM Profissionais p
            JOIN ElencoSerie es USING(id_profissional)
            JOIN Series s USING(id_serie)
            JOIN Serie_Genero sg USING(id_serie)
            JOIN Generos g USING(id_genero)
            JOIN Episodios e USING(id_serie)
            WHERE g.nome = 'Drama' AND e.duracao_segundos > 3000
        """
    },
    8: {
        "titulo": "Usuários que avaliaram filmes mas nunca séries",
        "descricao": "Usuários (e filmes avaliados) que nunca avaliaram nenhuma série.",
        "sql": """
            SELECT DISTINCT u.nome, f.titulo
            FROM Usuarios u
            JOIN AvaliacoesFilmes af USING(id_usuario)
            JOIN Filmes f USING(id_filme)
            WHERE u.id_usuario NOT IN (
                SELECT id_usuario FROM AvaliacoesSeries
            )
            ORDER BY u.nome ASC
        """
    },
    9: {
        "titulo": "Elenco de atores de uma saga  [PARÂMETRO]",
        "descricao": "Atores, personagens e filmes de uma saga específica.",
        "parametros": [
            {"label": "Nome da saga (ex: O Senhor dos Anéis)", "tipo": "str"}
        ],
        "sql": """
            SELECT p.nome AS ator, ef.personagem, f.titulo AS filme
            FROM Profissionais p
            NATURAL JOIN ElencoFilme ef
            NATURAL JOIN Filmes f
            WHERE f.saga = %s AND ef.papel = 'Ator'
        """
    },
    10: {
        "titulo": "Filmes com diretor e nota média antes de um ano  [PARÂMETRO]",
        "descricao": "Título, diretor e nota média de filmes lançados antes do ano informado.",
        "parametros": [
            {"label": "Ano (ex: 2005)", "tipo": "date_from_year"}
        ],
        "sql": """
            SELECT v.titulo, p.nome AS diretor, v.nota_media
            FROM view_media_filmes v
            JOIN Filmes f USING(id_filme)
            JOIN ElencoFilme ef USING(id_filme)
            JOIN Profissionais p USING(id_profissional)
            WHERE ef.papel = 'Diretor' AND f.lancamento < %s
        """
    },
}
