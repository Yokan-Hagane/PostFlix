#menu CLI
import db_con
import display
from consultas import CONSULTAS

def main():
    print("=== SISTEMA DE CATÁLOGO DE STREAMING ===")
    
    # Conecta com o banco
    try:
        conn = db_con.conectar()
        cur = conn.cursor()
        print("\nConexão bem sucedida!\n")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return

    # Menu
    while True:
        print("="*50)
        print("MENU DE CONSULTAS")
        print("="*50)
        for num, info in CONSULTAS.items():
            print(f"[{num}] {info['titulo']}")
        print("[0] Sair")
        
        escolha = input("\nEscolha uma opção: ").strip()
        
        if escolha == '0':
            print("Encerrando o sistema...")
            break
            
        if not escolha.isdigit() or int(escolha) not in CONSULTAS:
            print("Opção inválida! Tente novamente.")
            continue
            
        numero_consulta = int(escolha)
        consulta = CONSULTAS[numero_consulta]
        
        print("\n" + "-"*50)
        print(f"Executando: {consulta['descricao']}")
        print("-"*50)
        
        valores_parametros = []
        
        # Verifica se a consulta exige parâmetros e pede ao usuário
        if "parametros" in consulta:
            for param in consulta["parametros"]:
                valor_input = input(f"Digite o {param['label']}: ").strip()
                
                # Tratamento especial para o ano da consulta 10
                if param["tipo"] == "date_from_year":
                    # Converte o ano digitado (ex: '2005') para data completa ('2005-01-01')
                    valor_input = f"{valor_input}-01-01"
                    
                valores_parametros.append(valor_input)
        
        # Executa a query no banco de dados
        try:
            # O execute com a tupla de valores substitui os '%s' pelas variáveis de forma segura
            cur.execute(consulta["sql"], tuple(valores_parametros))
            
            display.tabela(cur)
            
        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")
            conn.rollback() # Desfaz qualquer transação com erro para não travar o banco

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
