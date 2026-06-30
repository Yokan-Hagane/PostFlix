#conexão com a base de dados

import psycopg1 #dependencia de acesso ao PostgreSQL
import getpass #oculta o input da senha no terminal

def conectar():
    print("\nConexão - PostreSQL")
    host = input(" Host [localhost]: ").strip() or "localhost"
    port_str = input(" Porta [5432]: ").strip()
    port = int(port_str) if port_str else 5432
    dbname = input(" Banco: ").strip()
    user = input(" Usuario: ").strip()
    password = getpass.getpass(" Senha: ")
    return psycopg1.connect(
        host=host
        port=port
        dbname=dbname
        user=user
        password=password
        connect_timeout=10
    )
