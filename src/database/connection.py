"""
Módulo de conexão com banco de dados SQLite para sistema da gráfica.

Este módulo fornece funções reutilizáveis para gerenciar conexões
e executar operações no banco de dados SQLite.

Autor: Sistema Gráfica
Data: 2025
"""

import sqlite3
import os
from typing import Optional, Any, List, Tuple


def get_connection() -> sqlite3.Connection:
    """
    Estabelece conexão com o banco de dados SQLite.
    
    Returns:
        sqlite3.Connection: Objeto de conexão com o banco de dados
        
    Raises:
        sqlite3.Error: Erro ao conectar com o banco de dados
    """
    try:
        # Caminho relativo para o arquivo do banco
        db_path = os.path.join('database', 'db.sqlite')
        
        # Verifica se o diretório existe
        if not os.path.exists('database'):
            os.makedirs('database')
        
        # Estabelece conexão com o banco
        conn = sqlite3.connect(db_path)
        
        # Configura para retornar resultados como Row (permite acesso por nome da coluna)
        conn.row_factory = sqlite3.Row
        
        print(f"✅ Conexão estabelecida com sucesso: {db_path}")
        return conn
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao conectar com o banco de dados: {e}")
        raise


def close_connection(conn: sqlite3.Connection) -> None:
    """
    Fecha a conexão com o banco de dados.
    
    Args:
        conn: Objeto de conexão a ser fechado
    """
    try:
        if conn:
            conn.close()
            print("✅ Conexão fechada com sucesso")
    except sqlite3.Error as e:
        print(f"❌ Erro ao fechar conexão: {e}")


def execute_query(query: str, params: Optional[Tuple] = None) -> Optional[List[sqlite3.Row]]:
    """
    Executa uma consulta SQL no banco de dados.
    
    Args:
        query: Comando SQL a ser executado
        params: Parâmetros para o comando SQL (opcional)
        
    Returns:
        List[sqlite3.Row]: Lista de resultados para SELECT, None para outros comandos
        
    Raises:
        sqlite3.Error: Erro na execução da consulta
    """
    conn = None
    try:
        # Estabelece conexão
        conn = get_connection()
        cursor = conn.cursor()
        
        # Executa a consulta com ou sem parâmetros
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Commit para operações que modificam dados
        if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
            conn.commit()
            affected_rows = cursor.rowcount
            print(f"✅ Consulta executada com sucesso. Linhas afetadas: {affected_rows}")
            return None
        
        # Retorna resultados para SELECT
        elif query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            print(f"✅ Consulta executada com sucesso. Registros encontrados: {len(results)}")
            return results
        
        # Para outros comandos (CREATE, DROP, etc.)
        else:
            conn.commit()
            print("✅ Comando executado com sucesso")
            return None
            
    except sqlite3.Error as e:
        print(f"❌ Erro na execução da consulta: {e}")
        print(f"Query: {query}")
        if params:
            print(f"Parâmetros: {params}")
        raise
        
    finally:
        # Garante que a conexão seja fechada
        if conn:
            close_connection(conn)


def execute_many(query: str, params_list: List[Tuple]) -> None:
    """
    Executa múltiplas operações SQL com diferentes parâmetros.
    
    Args:
        query: Comando SQL a ser executado
        params_list: Lista de tuplas com parâmetros para cada execução
        
    Raises:
        sqlite3.Error: Erro na execução das consultas
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Executa múltiplas operações
        cursor.executemany(query, params_list)
        conn.commit()
        
        affected_rows = cursor.rowcount
        print(f"✅ {len(params_list)} operações executadas com sucesso. Linhas afetadas: {affected_rows}")
        
    except sqlite3.Error as e:
        print(f"❌ Erro na execução múltipla: {e}")
        raise
        
    finally:
        if conn:
            close_connection(conn)


def test_connection() -> bool:
    """
    Testa a conexão com o banco de dados.
    
    Returns:
        bool: True se a conexão foi bem-sucedida, False caso contrário
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Executa uma consulta simples para testar
        cursor.execute("SELECT sqlite_version()")
        version = cursor.fetchone()[0]
        
        close_connection(conn)
        print(f"✅ Teste de conexão bem-sucedido. SQLite versão: {version}")
        return True
        
    except Exception as e:
        print(f"❌ Falha no teste de conexão: {e}")
        return False


if __name__ == "__main__":
    """
    Teste básico do módulo de conexão.
    """
    print("🔧 Testando módulo de conexão...")
    
    # Testa a conexão
    if test_connection():
        print("✅ Módulo de conexão funcionando corretamente!")
    else:
        print("❌ Problemas no módulo de conexão!")