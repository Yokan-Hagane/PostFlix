def tabela(cur):
    if cur.description is None:
        print(f"{cur.rowcount} linhas(s) afetada(s).")
        return

    colunas = [d[0] for d in cur.description]
    linhas = cur.fetchall()

    if not linhas:
        print("nenhum resultado")
        return

    larguras = [len(c) for c in colunas]
    for l in linhas:
        for i,v in enumerate(l):
            larguras[i] = max(larguras[i], len(str(v)))

    sep = "+-" + "-+-".join("-" * l for l in larguras) + "-+"
    fmt = "| " + " | ".join(f"{{:<{l}}}" for l in larguras) + " |"

    print(sep)
    print(fmt.format(*colunas))
    print(sep)
    for linha in linhas:
        print(fmt.format(*[str(v) for v in linha]))
    print(sep)
    print(f"({len(linhas)} linha(s))\n")
