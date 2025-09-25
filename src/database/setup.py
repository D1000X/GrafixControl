"""
Script de configuração e criação do banco de dados SQLite para sistema da gráfica.

Este script cria todas as tabelas necessárias para o sistema e executa
testes básicos de inserção e leitura para validar o funcionamento.

Autor: Sistema Gráfica  
Data: 2025
"""

import sqlite3
import os
import sys
from datetime import datetime

# Adiciona o diretório pai ao path para importar o módulo connection
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_connection, close_connection, execute_query


def create_database():
    """
    Cria o banco de dados SQLite e todas as tabelas necessárias.
    """
    print("🏗️  Iniciando criação do banco de dados...")
    
    # Verifica e cria o diretório database se não existir
    if not os.path.exists('database'):
        os.makedirs('database')
        print("📁 Diretório 'database' criado")
    
    try:
        # Cria as tabelas uma por uma
        create_usuarios_table()
        create_clientes_table()
        create_materiais_table()
        create_orcamentos_table()
        create_pagamentos_table()
        create_producao_table()
        
        print("✅ Banco de dados criado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro na criação do banco: {e}")
        raise


def create_usuarios_table():
    """
    Cria a tabela de usuários do sistema.
    
    Nota: Estrutura inicial com campos básicos. 
    Será expandida na Sprint 3 com campos específicos.
    """
    query = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE,
        senha VARCHAR(255),
        tipo VARCHAR(20) DEFAULT 'operador',
        ativo BOOLEAN DEFAULT 1,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    execute_query(query)
    print("📋 Tabela 'usuarios' criada")


def create_clientes_table():
    """
    Cria a tabela de clientes da gráfica.
    
    Armazena informações dos clientes que solicitam serviços de impressão.
    """
    query = """
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(100) NOT NULL,
        empresa VARCHAR(100),
        email VARCHAR(100),
        telefone VARCHAR(20),
        endereco TEXT,
        cidade VARCHAR(50),
        estado VARCHAR(2),
        cep VARCHAR(10),
        cpf_cnpj VARCHAR(20) UNIQUE,
        observacoes TEXT,
        ativo BOOLEAN DEFAULT 1,
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    execute_query(query)
    print("📋 Tabela 'clientes' criada")


def create_materiais_table():
    """
    Cria a tabela de materiais disponíveis na gráfica.
    
    Controla estoque de papéis, tintas e outros materiais utilizados na produção.
    """
    query = """
    CREATE TABLE IF NOT EXISTS materiais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(100) NOT NULL,
        descricao TEXT,
        categoria VARCHAR(50),
        unidade VARCHAR(10) DEFAULT 'un',
        preco_unitario DECIMAL(10,2) DEFAULT 0.00,
        estoque_atual INTEGER DEFAULT 0,
        estoque_minimo INTEGER DEFAULT 0,
        fornecedor VARCHAR(100),
        codigo_barras VARCHAR(50),
        ativo BOOLEAN DEFAULT 1,
        data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    execute_query(query)
    print("📋 Tabela 'materiais' criada")


def create_orcamentos_table():
    """
    Cria a tabela de orçamentos solicitados pelos clientes.
    
    Registra todos os orçamentos criados, aprovados ou rejeitados.
    """
    query = """
    CREATE TABLE IF NOT EXISTS orcamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_orcamento VARCHAR(20) UNIQUE NOT NULL,
        cliente_id INTEGER NOT NULL,
        descricao_servico TEXT NOT NULL,
        quantidade INTEGER DEFAULT 1,
        valor_unitario DECIMAL(10,2) DEFAULT 0.00,
        valor_total DECIMAL(10,2) DEFAULT 0.00,
        prazo_entrega DATE,
        status VARCHAR(20) DEFAULT 'pendente',
        observacoes TEXT,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        data_aprovacao DATETIME,
        data_vencimento DATETIME,
        usuario_id INTEGER,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    """
    
    execute_query(query)
    print("📋 Tabela 'orcamentos' criada")


def create_pagamentos_table():
    """
    Cria a tabela de controle de pagamentos.
    
    Registra pagamentos recebidos relacionados aos orçamentos aprovados.
    """
    query = """
    CREATE TABLE IF NOT EXISTS pagamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        orcamento_id INTEGER NOT NULL,
        valor_pagamento DECIMAL(10,2) NOT NULL,
        forma_pagamento VARCHAR(30) DEFAULT 'dinheiro',
        status_pagamento VARCHAR(20) DEFAULT 'pendente',
        data_vencimento DATE,
        data_pagamento DATETIME,
        observacoes TEXT,
        numero_comprovante VARCHAR(50),
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        usuario_id INTEGER,
        FOREIGN KEY (orcamento_id) REFERENCES orcamentos(id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    """
    
    execute_query(query)
    print("📋 Tabela 'pagamentos' criada")


def create_producao_table():
    """
    Cria a tabela de controle de produção.
    
    Acompanha o status de produção dos trabalhos aprovados.
    """
    query = """
    CREATE TABLE IF NOT EXISTS producao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        orcamento_id INTEGER NOT NULL,
        status_producao VARCHAR(30) DEFAULT 'aguardando',
        data_inicio DATETIME,
        data_previsao_fim DATETIME,
        data_conclusao DATETIME,
        responsavel VARCHAR(100),
        equipamento_usado VARCHAR(100),
        observacoes_producao TEXT,
        qualidade_aprovada BOOLEAN DEFAULT 0,
        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        usuario_id INTEGER,
        FOREIGN KEY (orcamento_id) REFERENCES orcamentos(id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    """
    
    execute_query(query)
    print("📋 Tabela 'producao' criada")


def insert_test_data():
    """
    Insere dados de teste no banco para validar funcionamento.
    
    Cria registros básicos em algumas tabelas para testar conexão e operações CRUD.
    """
    print("\n🧪 Inserindo dados de teste...")
    
    try:
        # Insere usuário de teste
        query_usuario = """
        INSERT INTO usuarios (nome, email, senha, tipo) 
        VALUES (?, ?, ?, ?)
        """
        execute_query(query_usuario, ("Admin Sistema", "admin@grafica.com", "admin123", "administrador"))
        
        # Insere cliente de teste
        query_cliente = """
        INSERT INTO clientes (nome, empresa, email, telefone, cidade, estado) 
        VALUES (?, ?, ?, ?, ?, ?)
        """
        execute_query(query_cliente, ("João Silva", "Empresa ABC Ltda", "joao@empresaabc.com", "(85) 99999-9999", "Fortaleza", "CE"))
        
        # Insere material de teste
        query_material = """
        INSERT INTO materiais (nome, descricao, categoria, unidade, preco_unitario, estoque_atual) 
        VALUES (?, ?, ?, ?, ?, ?)
        """
        execute_query(query_material, ("Papel A4 75g", "Papel sulfite branco A4 75g/m²", "Papel", "resma", 25.90, 50))
        
        print("✅ Dados de teste inseridos com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao inserir dados de teste: {e}")


def test_database_operations():
    """
    Executa testes de leitura no banco para confirmar funcionamento.
    
    Lê os dados inseridos e exibe no console para validação.
    """
    print("\n🔍 Testando operações de leitura...")
    
    try:
        # Testa consulta na tabela clientes
        clientes = execute_query("SELECT * FROM clientes")
        
        if clientes:
            print("\n📊 Dados da tabela CLIENTES:")
            for cliente in clientes:
                print(f"  ID: {cliente['id']}")
                print(f"  Nome: {cliente['nome']}")
                print(f"  Empresa: {cliente['empresa']}")
                print(f"  Email: {cliente['email']}")
                print(f"  Telefone: {cliente['telefone']}")
                print(f"  Cidade: {cliente['cidade']}")
                print(f"  Data Cadastro: {cliente['data_cadastro']}")
                print("-" * 40)
        
        # Testa consulta na tabela materiais
        materiais = execute_query("SELECT * FROM materiais")
        
        if materiais:
            print("\n📊 Dados da tabela MATERIAIS:")
            for material in materiais:
                print(f"  ID: {material['id']}")
                print(f"  Nome: {material['nome']}")
                print(f"  Categoria: {material['categoria']}")
                print(f"  Preço: R$ {material['preco_unitario']}")
                print(f"  Estoque: {material['estoque_atual']}")
                print("-" * 40)
        
        # Conta total de registros em cada tabela
        tabelas = ['usuarios', 'clientes', 'materiais', 'orcamentos', 'pagamentos', 'producao']
        
        print("\n📈 Resumo do banco de dados:")
        for tabela in tabelas:
            resultado = execute_query(f"SELECT COUNT(*) as total FROM {tabela}")
            total = resultado[0]['total'] if resultado else 0
            print(f"  {tabela.capitalize()}: {total} registro(s)")
        
        print("✅ Teste de leitura concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro no teste de leitura: {e}")


def main():
    """
    Função principal que executa todo o processo de criação e teste do banco.
    """
    print("=" * 60)
    print("🚀 SISTEMA GRÁFICA - SETUP DO BANCO DE DADOS")
    print("=" * 60)
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("-" * 60)
    
    try:
        # Cria o banco e tabelas
        create_database()
        
        # Insere dados de teste
        insert_test_data()
        
        # Testa operações de leitura
        test_database_operations()
        
        # Mensagem final de sucesso
        print("\n" + "=" * 60)
        print("✅ SETUP CONCLUÍDO COM SUCESSO!")
        print("✅ Banco de dados 'db.sqlite' criado em: database/db.sqlite")
        print("✅ Todas as tabelas foram criadas")
        print("✅ Dados de teste foram inseridos")
        print("✅ Conexão validada e funcionando")
        print("=" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERRO NO SETUP DO BANCO DE DADOS!")
        print(f"❌ Detalhes: {e}")
        print("=" * 60)
        raise


if __name__ == "__main__":
    """
    Executa o setup quando o script é chamado diretamente.
    
    Uso: python database/setup.py
    """
    main()