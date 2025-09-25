"""
Módulo de gerenciamento de usuários para sistema da gráfica.

Este módulo implementa todas as operações CRUD (Create, Read, Update, Delete)
para usuários do sistema, incluindo hash de senhas e validações.

Sprint 3 - Cadastro de Usuários
Autor: Sistema Gráfica
Data: 2025
"""

import hashlib
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# Adiciona o diretório pai ao path para importar connection
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import execute_query


def gerar_hash_senha(senha: str) -> str:
    """
    Gera hash SHA256 para a senha fornecida.
    
    Args:
        senha (str): Senha em texto puro
        
    Returns:
        str: Hash SHA256 da senha
        
    Exemplo:
        >>> hash_gerado = gerar_hash_senha("minha_senha123")
        >>> print(len(hash_gerado))  # 64 caracteres
        64
    """
    # Converte a senha para bytes e gera o hash SHA256
    senha_bytes = senha.encode('utf-8')
    hash_objeto = hashlib.sha256(senha_bytes)
    hash_hex = hash_objeto.hexdigest()
    
    print(f"🔐 Hash gerado para senha (primeiros 8 caracteres): {hash_hex[:8]}...")
    return hash_hex


def criar_usuario(nome: str, email: str, senha: str, perfil: str) -> bool:
    """
    Cria um novo usuário no sistema.
    
    Args:
        nome (str): Nome completo do usuário
        email (str): Email único do usuário
        senha (str): Senha em texto puro (será convertida para hash)
        perfil (str): Perfil do usuário ('admin' ou 'operador')
        
    Returns:
        bool: True se usuário foi criado com sucesso, False caso contrário
        
    Raises:
        ValueError: Se os parâmetros estiverem inválidos
        sqlite3.Error: Se houver erro no banco de dados
    """
    print(f"👤 Criando usuário: {nome} ({email}) - Perfil: {perfil}")
    
    # Validações básicas
    if not nome or not nome.strip():
        raise ValueError("Nome é obrigatório")
    
    if not email or not email.strip():
        raise ValueError("Email é obrigatório")
    
    if '@' not in email:
        raise ValueError("Email deve ter formato válido")
    
    if not senha or len(senha) < 4:
        raise ValueError("Senha deve ter pelo menos 4 caracteres")
    
    if perfil not in ['admin', 'operador']:
        raise ValueError("Perfil deve ser 'admin' ou 'operador'")
    
    try:
        # Verifica se email já existe
        usuario_existente = buscar_usuario_por_email(email)
        if usuario_existente:
            print(f"❌ Email {email} já está em uso")
            return False
        
        # Gera hash da senha
        senha_hash = gerar_hash_senha(senha)
        
        # Insere o novo usuário
        query = """
        INSERT INTO usuarios (nome, email, senha, perfil, data_criacao, data_atualizacao) 
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """
        
        execute_query(query, (nome.strip(), email.strip().lower(), senha_hash, perfil))
        
        print(f"✅ Usuário {nome} criado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário: {e}")
        return False


def listar_usuarios() -> List[Dict]:
    """
    Lista todos os usuários cadastrados no sistema.
    
    Returns:
        List[Dict]: Lista de dicionários com dados dos usuários
        
    Exemplo de retorno:
        [
            {
                'id': 1,
                'nome': 'Admin Sistema',
                'email': 'admin@grafica.com',
                'perfil': 'admin',
                'data_criacao': '2025-01-15 10:30:00'
            },
            ...
        ]
    """
    print("📋 Listando todos os usuários...")
    
    try:
        query = """
        SELECT id, nome, email, perfil, data_criacao, data_atualizacao 
        FROM usuarios 
        ORDER BY nome
        """
        
        resultado = execute_query(query)
        
        if not resultado:
            print("ℹ️  Nenhum usuário encontrado")
            return []
        
        # Converte sqlite3.Row para dicionários normais
        usuarios = []
        for row in resultado:
            usuario = {
                'id': row['id'],
                'nome': row['nome'],
                'email': row['email'],
                'perfil': row['perfil'],
                'data_criacao': row['data_criacao'],
                'data_atualizacao': row['data_atualizacao']
            }
            usuarios.append(usuario)
        
        print(f"✅ {len(usuarios)} usuário(s) encontrado(s)")
        return usuarios
        
    except Exception as e:
        print(f"❌ Erro ao listar usuários: {e}")
        return []


def buscar_usuario_por_email(email: str) -> Optional[Dict]:
    """
    Busca um usuário específico pelo email.
    
    Args:
        email (str): Email do usuário a ser buscado
        
    Returns:
        Dict ou None: Dados do usuário se encontrado, None caso contrário
        
    Exemplo:
        >>> usuario = buscar_usuario_por_email("admin@grafica.com")
        >>> if usuario:
        ...     print(f"Usuário: {usuario['nome']}")
    """
    print(f"🔍 Buscando usuário por email: {email}")
    
    if not email or not email.strip():
        print("❌ Email não fornecido")
        return None
    
    try:
        query = """
        SELECT id, nome, email, senha, perfil, data_criacao, data_atualizacao 
        FROM usuarios 
        WHERE LOWER(email) = LOWER(?)
        """
        
        resultado = execute_query(query, (email.strip(),))
        
        if not resultado:
            print(f"ℹ️  Usuário com email {email} não encontrado")
            return None
        
        # Pega o primeiro resultado (email é único)
        row = resultado[0]
        usuario = {
            'id': row['id'],
            'nome': row['nome'],
            'email': row['email'],
            'senha': row['senha'],  # Hash - nunca exibir em logs
            'perfil': row['perfil'],
            'data_criacao': row['data_criacao'],
            'data_atualizacao': row['data_atualizacao']
        }
        
        print(f"✅ Usuário encontrado: {usuario['nome']} - Perfil: {usuario['perfil']}")
        return usuario
        
    except Exception as e:
        print(f"❌ Erro ao buscar usuário: {e}")
        return None


def buscar_usuario_por_id(id_usuario: int) -> Optional[Dict]:
    """
    Busca um usuário específico pelo ID.
    
    Args:
        id_usuario (int): ID do usuário
        
    Returns:
        Dict ou None: Dados do usuário se encontrado, None caso contrário
    """
    print(f"🔍 Buscando usuário por ID: {id_usuario}")
    
    if not id_usuario or id_usuario <= 0:
        print("❌ ID inválido")
        return None
    
    try:
        query = """
        SELECT id, nome, email, perfil, data_criacao, data_atualizacao 
        FROM usuarios 
        WHERE id = ?
        """
        
        resultado = execute_query(query, (id_usuario,))
        
        if not resultado:
            print(f"ℹ️  Usuário com ID {id_usuario} não encontrado")
            return None
        
        row = resultado[0]
        usuario = {
            'id': row['id'],
            'nome': row['nome'],
            'email': row['email'],
            'perfil': row['perfil'],
            'data_criacao': row['data_criacao'],
            'data_atualizacao': row['data_atualizacao']
        }
        
        print(f"✅ Usuário encontrado: {usuario['nome']}")
        return usuario
        
    except Exception as e:
        print(f"❌ Erro ao buscar usuário por ID: {e}")
        return None


def atualizar_usuario(id_usuario: int, nome: str = None, email: str = None, 
                     senha: str = None, perfil: str = None) -> bool:
    """
    Atualiza dados de um usuário existente.
    
    Args:
        id_usuario (int): ID do usuário a ser atualizado
        nome (str, optional): Novo nome
        email (str, optional): Novo email
        senha (str, optional): Nova senha (será convertida para hash)
        perfil (str, optional): Novo perfil ('admin' ou 'operador')
        
    Returns:
        bool: True se atualização foi bem-sucedida, False caso contrário
        
    Exemplo:
        >>> # Atualizar apenas o nome
        >>> sucesso = atualizar_usuario(1, nome="Novo Nome")
        
        >>> # Atualizar nome e senha
        >>> sucesso = atualizar_usuario(1, nome="João", senha="nova_senha123")
    """
    print(f"✏️  Atualizando usuário ID: {id_usuario}")
    
    if not id_usuario or id_usuario <= 0:
        print("❌ ID de usuário inválido")
        return False
    
    # Verifica se usuário existe
    usuario_atual = buscar_usuario_por_id(id_usuario)
    if not usuario_atual:
        print(f"❌ Usuário com ID {id_usuario} não encontrado")
        return False
    
    try:
        # Monta query dinâmica baseada nos campos fornecidos
        campos_update = []
        parametros = []
        
        if nome is not None and nome.strip():
            campos_update.append("nome = ?")
            parametros.append(nome.strip())
        
        if email is not None and email.strip():
            # Verifica se novo email já existe (em outro usuário)
            if email.lower() != usuario_atual['email'].lower():
                usuario_email_existente = buscar_usuario_por_email(email)
                if usuario_email_existente:
                    print(f"❌ Email {email} já está em uso por outro usuário")
                    return False
            
            if '@' not in email:
                print("❌ Email deve ter formato válido")
                return False
                
            campos_update.append("email = ?")
            parametros.append(email.strip().lower())
        
        if senha is not None and senha.strip():
            if len(senha) < 4:
                print("❌ Senha deve ter pelo menos 4 caracteres")
                return False
                
            senha_hash = gerar_hash_senha(senha)
            campos_update.append("senha = ?")
            parametros.append(senha_hash)
        
        if perfil is not None and perfil.strip():
            if perfil not in ['admin', 'operador']:
                print("❌ Perfil deve ser 'admin' ou 'operador'")
                return False
                
            campos_update.append("perfil = ?")
            parametros.append(perfil)
        
        # Se nenhum campo foi fornecido para atualização
        if not campos_update:
            print("ℹ️  Nenhum campo fornecido para atualização")
            return False
        
        # Adiciona data de atualização
        campos_update.append("data_atualizacao = CURRENT_TIMESTAMP")
        parametros.append(id_usuario)  # Para a cláusula WHERE
        
        # Monta e executa query
        query = f"""
        UPDATE usuarios 
        SET {', '.join(campos_update)} 
        WHERE id = ?
        """
        
        execute_query(query, tuple(parametros))
        
        print(f"✅ Usuário ID {id_usuario} atualizado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar usuário: {e}")
        return False


def deletar_usuario(id_usuario: int) -> bool:
    """
    Remove um usuário do sistema.
    
    Args:
        id_usuario (int): ID do usuário a ser removido
        
    Returns:
        bool: True se usuário foi removido com sucesso, False caso contrário
        
    Nota:
        Esta operação é irreversível. Use com cuidado!
    """
    print(f"🗑️  Deletando usuário ID: {id_usuario}")
    
    if not id_usuario or id_usuario <= 0:
        print("❌ ID de usuário inválido")
        return False
    
    try:
        # Verifica se usuário existe antes de deletar
        usuario = buscar_usuario_por_id(id_usuario)
        if not usuario:
            print(f"❌ Usuário com ID {id_usuario} não encontrado")
            return False
        
        # Executa a exclusão
        query = "DELETE FROM usuarios WHERE id = ?"
        execute_query(query, (id_usuario,))
        
        print(f"✅ Usuário '{usuario['nome']}' removido com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao deletar usuário: {e}")
        return False


def verificar_login(email: str, senha: str) -> Optional[Dict]:
    """
    Verifica credenciais de login do usuário.
    
    Args:
        email (str): Email do usuário
        senha (str): Senha em texto puro
        
    Returns:
        Dict ou None: Dados do usuário se login válido, None caso contrário
        
    Exemplo:
        >>> usuario = verificar_login("admin@grafica.com", "admin123")
        >>> if usuario:
        ...     print(f"Login válido: {usuario['nome']}")
    """
    print(f"🔐 Verificando login para: {email}")
    
    if not email or not senha:
        print("❌ Email e senha são obrigatórios")
        return None
    
    try:
        # Busca usuário pelo email
        usuario = buscar_usuario_por_email(email)
        if not usuario:
            print("❌ Usuário não encontrado")
            return None
        
        # Verifica senha
        senha_hash = gerar_hash_senha(senha)
        if senha_hash == usuario['senha']:
            print(f"✅ Login válido para {usuario['nome']} - Perfil: {usuario['perfil']}")
            # Remove a senha do retorno por segurança
            del usuario['senha']
            return usuario
        else:
            print("❌ Senha incorreta")
            return None
            
    except Exception as e:
        print(f"❌ Erro na verificação de login: {e}")
        return None


def contar_usuarios() -> int:
    """
    Conta o total de usuários cadastrados.
    
    Returns:
        int: Número total de usuários
    """
    try:
        resultado = execute_query("SELECT COUNT(*) as total FROM usuarios")
        return resultado[0]['total'] if resultado else 0
    except Exception as e:
        print(f"❌ Erro ao contar usuários: {e}")
        return 0


def listar_usuarios_por_perfil(perfil: str) -> List[Dict]:
    """
    Lista usuários filtrados por perfil.
    
    Args:
        perfil (str): Perfil a filtrar ('admin' ou 'operador')
        
    Returns:
        List[Dict]: Lista de usuários do perfil especificado
    """
    print(f"📋 Listando usuários com perfil: {perfil}")
    
    if perfil not in ['admin', 'operador']:
        print("❌ Perfil deve ser 'admin' ou 'operador'")
        return []
    
    try:
        query = """
        SELECT id, nome, email, perfil, data_criacao, data_atualizacao 
        FROM usuarios 
        WHERE perfil = ? 
        ORDER BY nome
        """
        
        resultado = execute_query(query, (perfil,))
        
        if not resultado:
            print(f"ℹ️  Nenhum usuário encontrado com perfil {perfil}")
            return []
        
        usuarios = []
        for row in resultado:
            usuario = {
                'id': row['id'],
                'nome': row['nome'],
                'email': row['email'],
                'perfil': row['perfil'],
                'data_criacao': row['data_criacao'],
                'data_atualizacao': row['data_atualizacao']
            }
            usuarios.append(usuario)
        
        print(f"✅ {len(usuarios)} usuário(s) encontrado(s) com perfil {perfil}")
        return usuarios
        
    except Exception as e:
        print(f"❌ Erro ao listar usuários por perfil: {e}")
        return []


# ========================================================================================
# TESTES E EXECUÇÃO PRINCIPAL
# ========================================================================================

def executar_testes():
    """
    Executa testes básicos do módulo de usuários.
    """
    print("\n" + "=" * 60)
    print("🧪 EXECUTANDO TESTES DO MÓDULO DE USUÁRIOS")
    print("=" * 60)
    
    try:
        print("\n1️⃣ Teste: Criar usuário de teste")
        sucesso = criar_usuario(
            nome="Operador Teste",
            email="operador@grafica.com", 
            senha="teste123",
            perfil="operador"
        )
        print(f"Resultado: {'✅ Sucesso' if sucesso else '❌ Falha'}")
        
        print("\n2️⃣ Teste: Listar todos os usuários")
        usuarios = listar_usuarios()
        for usuario in usuarios:
            print(f"  - {usuario['nome']} ({usuario['email']}) - {usuario['perfil']}")
        
        print("\n3️⃣ Teste: Buscar usuário por email")
        usuario = buscar_usuario_por_email("operador@grafica.com")
        if usuario:
            print(f"  Encontrado: {usuario['nome']} - Perfil: {usuario['perfil']}")
        
        print("\n4️⃣ Teste: Atualizar usuário")
        if usuario:
            sucesso = atualizar_usuario(usuario['id'], nome="Operador Atualizado")
            print(f"Resultado: {'✅ Sucesso' if sucesso else '❌ Falha'}")
        
        print("\n5️⃣ Teste: Verificar login")
        login_valido = verificar_login("operador@grafica.com", "teste123")
        if login_valido:
            print(f"  Login válido: {login_valido['nome']}")
        
        print("\n6️⃣ Teste: Contar usuários")
        total = contar_usuarios()
        print(f"  Total de usuários: {total}")
        
        print("\n" + "=" * 60)
        print("✅ TESTES CONCLUÍDOS COM SUCESSO!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        print("=" * 60)


if __name__ == "__main__":
    """
    Executa testes quando o módulo é chamado diretamente.
    
    Uso: python modules/usuarios.py
    """
    executar_testes()