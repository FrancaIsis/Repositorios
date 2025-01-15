import sqlite3  # biblioteca para trabalhar com bancos de dados SQLite
from prettytable import PrettyTable  # tabelas formatadas
# importar o modulo pathlib para trabalhar com caminhos relativos ou absolutos
from pathlib import Path
import os


os.system('cls')
# conexao com o banco de dados

# caminho relativo
db_path = Path('BD') / 'bd_rel_1_n.db'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# criação da tabela 'Clientes' (Tabela principal)
cursor.execute('''
               CREATE TABLE IF NOT EXISTS Clientes (
                   id_cliente INTEGER PRIMARY KEY AUTOINCREMENT, -- ID unico para o cliente
                   nome TEXT NOT NULL,                           -- Nome do cliente
                   email TEXT UNIQUE NOT NULL,                   -- Email unico
                   telefone TEXT,                                -- Telefone do cliente
                   cidade TEXT                                   -- Cidade onde mora
               )
               ''')
# Criação tabela pedidos (tabela relacionada)
cursor.execute('''
               CREATE TABLE IF NOT EXISTS Pedidos (
                   id_pedido INTEGER PRIMARY KEY AUTOINCREMENT, -- ID unico para o pedido
                   id_cliente INTEGER NOT NULL,                 -- Relacionamento com a tabela Clientes
                   produto TEXT NOT NULL,                       -- Nome do produto pedido
                   quantidade INTEGER NOT NULL,                 -- Quantidade do produto 
                   data TEXT NOT NULL,                          -- Data do pedido
                   valor_total REAL NOT NULL,                   -- Valor total do pedido
                   FOREIGN KEY (id_cliente) REFERENCES Clientes (id_cliente) -- Chave estrangeira
               )
               ''')
# Função para verificar se um cliente existe no banco de dados


def cliente_existe(id_cliente):
    cursor.execute(
        'SELECT 1 FROM Clientes WHERE id_cliente = ?', (id_cliente,)
    )
    # Retorna True se o cliente existir, False caso contrário
    return cursor.fetchone() is not None

# Função para inserir dados na tabela Clientes


def inserir_cliente():
    nome = input('Digite o nome do cliente: ')
    email = input('Digite o email do cliente: ')
    telefone = input('Digite o telefone do cliente: ')
    cidade = input('Digite a cidade do cliente: ')
    cursor.execute('''
                   INSERT INTO Clientes (nome, email, telefone, cidade)
                   VALUES (?,?,?,?)
                   ''', (nome, email, telefone, cidade))
    conn.commit()
    print('Cliente inserido com sucesso!!')

# Função para inserir dados na tabela Pedidos


def inserir_pedido():
    # listando os clientes
    cursor.execute('''
                   SELECT * FROM clientes
                   ''')
    resultados = cursor.fetchall()

    # não posso fazer pedidos sem clientes
    if not resultados:
        print('-' * 70)
        print('Nenhum cliente encontrado. Cadastre um cliente primeiro.')
        print('-' * 70)
        return
    # criar e formatar tabela para exibição
    tabela = PrettyTable(['id_cliente', 'Nome', 'Email', 'Telefone', 'Cidade'])
    for linha in resultados:
        tabela.add_rows(linha)
    print(tabela)

    try:
        # Garantir que o ID seja um numero inteiro
        id_cliente = int(input('Digite o ID do cliente: '))
        # Verificar se o cliente existe antes de prosseguir
        if not cliente_existe(id_cliente):
            print('-' * 70)
            print(f'Erro: Cliente com ID {id_cliente} não encontrado!')
            print('Por favor, cadastr o cliente primeiro.')
            print('-' * 70)
            # Retorna ao menu se o cliente não existir
            return

        # Solicitar dados so pedido
        produto = input('Digite o nome do produto: ')
        quantidade = int(input('Digite a quantidade: '))
        # ISO 8601(YYYY-MM-DD)
        data = input('Digite a data do pedido(YYYY-MM-DD):')
        valor_total = float(input('Digite o valor total: '))

        # Inserir o pedido no banco de dados
        cursor.execute('''
                       INSERT INTO Pedidos (id_cliente, produto, quantidade, data, valor_total)
                       VALUES(?,?,?,?,?)
                       ''', (id_cliente, produto, quantidade, data, valor_total))
        conn.commit()
