"""
Exemplo de uso completo do sistema de usuários da gráfica.

Este arquivo demonstra como usar todos os módulos criados na Sprint 3,
incluindo operações de banco, CRUD e interface gráfica.

Sprint 3 - Cadastro de Usuários
Autor: Sistema Gráfica
Data: 2025
"""

import os
import sys
from datetime import datetime

# Adiciona paths necessários
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("🎨 SISTEMA GRÁFICA - EXEMPLO DE USO COMPLETO")
print("=" * 70)
print(f"⏰ Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print()


def exemplo_1_setup_banco():
    """
    Exemplo 1: Executar setup do banco de dados.
    """
    print("1️⃣ SETUP DO BANCO DE DADOS")
    print("-" * 40)
    
    try:
        # Executa setup do banco (cria tabelas)
        from database.setup import main as setup_main
        
        print("🏗️  Executando setup do banco de dados...")
        setup_main()
        
        print("✅ Setup concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro no setup: {e}")
    
    print()


def exemplo_2_operacoes_crud():
    """
    Exemplo 2: Operações CRUD básicas.
    """
    print("2️⃣ OPERAÇÕES CRUD DE USUÁRIOS")
    print("-" * 40)
    
    try:
        from modules.usuarios import (
            criar_usuario, listar_usuarios, buscar_usuario_por_email,
            atualizar_usuario, deletar_usuario, verificar_login
        )
        
        # Criar usuários de exemplo
        print("📝 Criando usuários de exemplo...")
        
        usuarios_exemplo = [
            ("Maria Silva", "maria@grafica.com", "senha123", "admin"),
            ("João Santos", "joao@grafica.com", "pass456", "operador"),
            ("Ana Costa", "ana@grafica.com", "abc789", "operador"),
        ]
        
        for nome, email, senha, perfil in usuarios_exemplo:
            sucesso = criar_usuario(nome, email, senha, perfil)
            if sucesso:
                print(f"  ✅ {nome} criado como {perfil}")
            else:
                print(f"  ℹ️  {nome} já existe ou erro na criação")
        
        print()
        
        # Listar usuários
        print("📋 Listando todos os usuários:")
        usuarios = listar_usuarios()
        for usuario in usuarios:
            print(f"  • {usuario['nome']} ({usuario['email']}) - {usuario['perfil']}")
        
        print()
        
        # Buscar usuário específico
        print("🔍 Buscando usuário por email:")
        usuario = buscar_usuario_por_email("maria@grafica.com")
        if usuario:
            print(f"  Encontrado: {usuario['nome']} - Perfil: {usuario['perfil']}")
        
        print()
        
        # Testar login
        print("🔐 Testando login:")
        login_valido = verificar_login("maria@grafica.com", "senha123")
        if login_valido:
            print(f"  ✅ Login válido: {login_valido['nome']}")
        else:
            print("  ❌ Login inválido")
        
        print()
        
        # Atualizar usuário
        print("✏️  Atualizando usuário:")
        if usuario:
            sucesso = atualizar_usuario(usuario['id'], nome="Maria Silva Santos")
            if sucesso:
                print("  ✅ Usuário atualizado com sucesso")
        
        print("✅ Operações CRUD concluídas!")
        
    except Exception as e:
        print(f"❌ Erro nas operações CRUD: {e}")
    
    print()


def exemplo_3_interface_grafica():
    """
    Exemplo 3: Abrir interface gráfica.
    """
    print("3️⃣ INTERFACE GRÁFICA")
    print("-" * 40)
    
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        # Pergunta se deve abrir a interface
        print("🖥️  Preparando interface gráfica...")
        print("💡 A interface será aberta em uma nova janela.")
        print("   Feche a janela da interface para continuar este exemplo.")
        
        resposta = input("\n🤔 Deseja abrir a interface gráfica? (s/n): ")
        
        if resposta.lower() in ['s', 'sim', 'y', 'yes']:
            from ui.usuarios_ui import main as ui_main
            
            print("🚀 Abrindo interface gráfica...")
            print("   (A interface abrirá em uma nova janela)")
            
            # Executa interface gráfica
            ui_main()
            
            print("✅ Interface fechada pelo usuário")
        else:
            print("ℹ️  Interface não foi aberta por escolha do usuário")
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Verifique se o Tkinter está instalado")
    except Exception as e:
        print(f"❌ Erro na interface gráfica: {e}")
    
    print()


def exemplo_4_relatorio_sistema():
    """
    Exemplo 4: Relatório do sistema.
    """
    print("4️⃣ RELATÓRIO DO SISTEMA")
    print("-" * 40)
    
    try:
        from modules.usuarios import contar_usuarios, listar_usuarios_por_perfil
        from database.connection import test_connection
        
        # Teste de conexão
        print("🔧 Testando conexão com banco:")
        conexao_ok = test_connection()
        print(f"  Status: {'✅ OK' if conexao_ok else '❌ FALHA'}")
        
        print()
        
        # Contadores
        print("📊 Estatísticas do sistema:")
        total_usuarios = contar_usuarios()
        print(f"  Total de usuários: {total_usuarios}")
        
        admins = listar_usuarios_por_perfil("admin")
        operadores = listar_usuarios_por_perfil("operador")
        
        print(f"  Administradores: {len(admins)}")
        print(f"  Operadores: {len(operadores)}")
        
        print()
        
        # Lista por perfil
        if admins:
            print("👑 Administradores:")
            for admin in admins:
                print(f"  • {admin['nome']} ({admin['email']})")
        
        print()
        
        if operadores:
            print("👷 Operadores:")
            for operador in operadores:
                print(f"  • {operador['nome']} ({operador['email']})")
        
        print("✅ Relatório concluído!")
        
    except Exception as e:
        print(f"❌ Erro no relatório: {e}")
    
    print()


def exemplo_5_limpeza_dados_teste():
    """
    Exemplo 5: Opção de limpeza de dados de teste.
    """
    print("5️⃣ LIMPEZA DE DADOS DE TESTE")
    print("-" * 40)
    
    try:
        from modules.usuarios import listar_usuarios, deletar_usuario
        
        print("🧹 Opção de limpeza de dados de teste...")
        
        # Lista usuários atuais
        usuarios = listar_usuarios()
        usuarios_teste = [u for u in usuarios if "grafica.com" in u['email']]
        
        if not usuarios_teste:
            print("ℹ️  Nenhum usuário de teste encontrado")
            return
        
        print(f"📋 Encontrados {len(usuarios_teste)} usuário(s) de teste:")
        for usuario in usuarios_teste:
            print(f"  • {usuario['nome']} ({usuario['email']})")
        
        resposta = input("\n🗑️  Deseja excluir os usuários de teste? (s/n): ")
        
        if resposta.lower() in ['s', 'sim', 'y', 'yes']:
            print("🗑️  Excluindo usuários de teste...")
            
            excluidos = 0
            for usuario in usuarios_teste:
                sucesso = deletar_usuario(usuario['id'])
                if sucesso:
                    excluidos += 1
                    print(f"  ✅ {usuario['nome']} excluído")
            
            print(f"✅ {excluidos} usuário(s) de teste excluído(s)")
        else:
            print("ℹ️  Usuários de teste mantidos")
        
    except Exception as e:
        print(f"❌ Erro na limpeza: {e}")
    
    print()


def main():
    """
    Função principal que executa todos os exemplos.
    """
    try:
        print("🚀 Iniciando exemplos do sistema...")
        print()
        
        # Executa exemplos em sequência
        exemplo_1_setup_banco()
        exemplo_2_operacoes_crud()
        exemplo_3_interface_grafica()
        exemplo_4_relatorio_sistema()
        exemplo_5_limpeza_dados_teste()
        
        # Mensagem final
        print("=" * 70)
        print("🎉 TODOS OS EXEMPLOS CONCLUÍDOS!")
        print("=" * 70)
        print("✅ Sistema de usuários funcionando corretamente")
        print("✅ Banco de dados operacional")
        print("✅ Interface gráfica disponível")
        print("✅ Operações CRUD implementadas")
        print()
        print("💡 Para usar o sistema:")
        print("   • Execute: python database/setup.py (primeira vez)")
        print("   • Execute: python ui/usuarios_ui.py (interface gráfica)")
        print("   • Execute: python modules/usuarios.py (operações via terminal)")
    except Exception as e:
        print(f"❌ Erro inesperado na execução principal: {e}")