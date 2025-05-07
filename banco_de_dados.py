import sqlite3

def conectar():
    return sqlite3.connect("estoque.db")

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    # Criando a tabela estoque com a coluna "tipo"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL,
            tipo TEXT NOT NULL  -- Nova coluna adicionada
        )
    ''')

    conexao.commit()
    conexao.close()

# Executa a criação da tabela ao rodar o programa
criar_tabela()
