"""
Interface gráfica Tkinter para gerenciamento de usuários.

Esta interface permite cadastrar, listar, atualizar e excluir usuários
do sistema da gráfica de forma visual e intuitiva.

Sprint 3 - Cadastro de Usuários
Autor: Sistema Gráfica
Data: 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import sys
from typing import List, Dict, Optional

# Adiciona o diretório pai ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa funções do módulo de usuários
from modules.usuarios import (
    criar_usuario, listar_usuarios, buscar_usuario_por_email,
    atualizar_usuario, deletar_usuario, verificar_login,
    contar_usuarios, listar_usuarios_por_perfil
)


class UsuariosUI:
    """
    Classe principal da interface de usuários.
    
    Gerencia toda a interface gráfica e interage com o módulo de usuários
    para executar operações CRUD.
    """
    
    def __init__(self, root: tk.Tk):
        """
        Inicializa a interface gráfica.
        
        Args:
            root: Janela principal do Tkinter
        """
        self.root = root
        self.usuario_selecionado_id = None  # ID do usuário selecionado na lista
        
        # Configurações da janela principal
        self.configurar_janela_principal()
        
        # Cria os elementos da interface
        self.criar_interface()
        
        # Carrega dados iniciais
        self.atualizar_lista_usuarios()
        
        print("🖥️  Interface de usuários iniciada")
    
    def configurar_janela_principal(self):
        """
        Configura as propriedades da janela principal.
        """
        self.root.title("Sistema Gráfica - Gerenciamento de Usuários")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Define ícone se existir (opcional)
        try:
            # self.root.iconbitmap("icon.ico")  # Descomente se tiver um ícone
            pass
        except:
            pass
        
        # Centraliza a janela na tela
        self.centralizar_janela()
    
    def centralizar_janela(self):
        """
        Centraliza a janela na tela do usuário.
        """
        # Atualiza para obter dimensões corretas
        self.root.update_idletasks()
        
        # Obtém dimensões da tela e da janela
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        largura_janela = self.root.winfo_reqwidth()
        altura_janela = self.root.winfo_reqheight()
        
        # Calcula posição central
        x = (largura_tela - 800) // 2
        y = (altura_tela - 600) // 2
        
        # Define posição
        self.root.geometry(f"800x600+{x}+{y}")
    
    def criar_interface(self):
        """
        Cria todos os elementos da interface gráfica.
        """
        # Frame principal com padding
        self.frame_principal = ttk.Frame(self.root, padding="10")
        self.frame_principal.grid(row=0, column=0, sticky="nsew")
        
        # Configura redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.frame_principal.columnconfigure(1, weight=1)
        self.frame_principal.rowconfigure(2, weight=1)
        
        # Cria seções da interface
        self.criar_titulo()
        self.criar_formulario()
        self.criar_lista_usuarios()
        self.criar_botoes_acao()
        self.criar_barra_status()
    
    def criar_titulo(self):
        """
        Cria o título da aplicação.
        """
        titulo = ttk.Label(
            self.frame_principal, 
            text="🎨 Sistema Gráfica - Gerenciamento de Usuários",
            font=("Arial", 16, "bold")
        )
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
    
    def criar_formulario(self):
        """
        Cria o formulário de cadastro/edição de usuários.
        """
        # Frame do formulário
        self.frame_formulario = ttk.LabelFrame(
            self.frame_principal, 
            text="📝 Dados do Usuário", 
            padding="10"
        )
        self.frame_formulario.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Variáveis dos campos
        self.var_nome = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_senha = tk.StringVar()
        self.var_perfil = tk.StringVar(value="operador")
        
        # Campo Nome
        ttk.Label(self.frame_formulario, text="Nome:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_nome = ttk.Entry(
            self.frame_formulario, 
            textvariable=self.var_nome, 
            width=30
        )
        self.entry_nome.grid(row=0, column=1, sticky="ew", padx=(5, 10), pady=2)
        
        # Campo Email
        ttk.Label(self.frame_formulario, text="Email:").grid(row=0, column=2, sticky="w", pady=2)
        self.entry_email = ttk.Entry(
            self.frame_formulario, 
            textvariable=self.var_email, 
            width=30
        )
        self.entry_email.grid(row=0, column=3, sticky="ew", padx=(5, 0), pady=2)
        
        # Campo Senha
        ttk.Label(self.frame_formulario, text="Senha:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_senha = ttk.Entry(
            self.frame_formulario, 
            textvariable=self.var_senha, 
            show="*",  # Oculta a senha
            width=30
        )
        self.entry_senha.grid(row=1, column=1, sticky="ew", padx=(5, 10), pady=2)
        
        # Campo Perfil (ComboBox)
        ttk.Label(self.frame_formulario, text="Perfil:").grid(row=1, column=2, sticky="w", pady=2)
        self.combo_perfil = ttk.Combobox(
            self.frame_formulario,
            textvariable=self.var_perfil,
            values=["admin", "operador"],
            state="readonly",
            width=27
        )
        self.combo_perfil.grid(row=1, column=3, sticky="ew", padx=(5, 0), pady=2)
        
        # Configura redimensionamento do formulário
        self.frame_formulario.columnconfigure(1, weight=1)
        self.frame_formulario.columnconfigure(3, weight=1)
    
    def criar_lista_usuarios(self):
        """
        Cria a área de listagem de usuários com Treeview.
        """
        # Frame da lista
        self.frame_lista = ttk.LabelFrame(
            self.frame_principal, 
            text="👥 Usuários Cadastrados", 
            padding="10"
        )
        self.frame_lista.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        
        # Configura redimensionamento
        self.frame_lista.columnconfigure(0, weight=1)
        self.frame_lista.rowconfigure(0, weight=1)
        
        # Cria Treeview para exibir usuários
        colunas = ("ID", "Nome", "Email", "Perfil", "Data Cadastro")
        self.tree_usuarios = ttk.Treeview(
            self.frame_lista,
            columns=colunas,
            show="headings",
            height=12
        )
        
        # Configura cabeçalhos das colunas
        self.tree_usuarios.heading("ID", text="ID")
        self.tree_usuarios.heading("Nome", text="Nome")
        self.tree_usuarios.heading("Email", text="Email")
        self.tree_usuarios.heading("Perfil", text="Perfil")
        self.tree_usuarios.heading("Data Cadastro", text="Data Cadastro")
        
        # Configura largura das colunas
        self.tree_usuarios.column("ID", width=50, minwidth=50)
        self.tree_usuarios.column("Nome", width=200, minwidth=150)
        self.tree_usuarios.column("Email", width=250, minwidth=200)
        self.tree_usuarios.column("Perfil", width=100, minwidth=80)
        self.tree_usuarios.column("Data Cadastro", width=150, minwidth=120)
        
        # Adiciona barras de rolagem
        scrollbar_vertical = ttk.Scrollbar(
            self.frame_lista, 
            orient="vertical", 
            command=self.tree_usuarios.yview
        )
        scrollbar_horizontal = ttk.Scrollbar(
            self.frame_lista, 
            orient="horizontal", 
            command=self.tree_usuarios.xview
        )
        
        self.tree_usuarios.configure(
            yscrollcommand=scrollbar_vertical.set,
            xscrollcommand=scrollbar_horizontal.set
        )
        
        # Posiciona elementos
        self.tree_usuarios.grid(row=0, column=0, sticky="nsew")
        scrollbar_vertical.grid(row=0, column=1, sticky="ns")
        scrollbar_horizontal.grid(row=1, column=0, sticky="ew")
        
        # Bind evento de seleção
        self.tree_usuarios.bind("<<TreeviewSelect>>", self.on_usuario_selecionado)
    
    def criar_botoes_acao(self):
        """
        Cria os botões de ação (Adicionar, Atualizar, Excluir, etc.).
        """
        # Frame dos botões
        self.frame_botoes = ttk.Frame(self.frame_principal)
        self.frame_botoes.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        # Botão Adicionar
        self.btn_adicionar = ttk.Button(
            self.frame_botoes,
            text="➕ Adicionar",
            command=self.adicionar_usuario
        )
        self.btn_adicionar.grid(row=0, column=0, padx=(0, 5))
        
        # Botão Atualizar
        self.btn_atualizar = ttk.Button(
            self.frame_botoes,
            text="✏️ Atualizar",
            command=self.atualizar_usuario_selecionado,
            state="disabled"
        )
        self.btn_atualizar.grid(row=0, column=1, padx=5)
        
        # Botão Excluir
        self.btn_excluir = ttk.Button(
            self.frame_botoes,
            text="🗑️ Excluir",
            command=self.excluir_usuario_selecionado,
            state="disabled"
        )
        self.btn_excluir.grid(row=0, column=2, padx=5)
        
        # Botão Limpar Formulário
        self.btn_limpar = ttk.Button(
            self.frame_botoes,
            text="🧹 Limpar",
            command=self.limpar_formulario
        )
        self.btn_limpar.grid(row=0, column=3, padx=5)
        
        # Botão Atualizar Lista
        self.btn_atualizar_lista = ttk.Button(
            self.frame_botoes,
            text="🔄 Atualizar Lista",
            command=self.atualizar_lista_usuarios
        )
        self.btn_atualizar_lista.grid(row=0, column=4, padx=(5, 0))
    
    def criar_barra_status(self):
        """
        Cria a barra de status na parte inferior.
        """
        self.frame_status = ttk.Frame(self.frame_principal)
        self.frame_status.grid(row=4, column=0, columnspan=2, sticky="ew")
        
        # Label de status
        self.label_status = ttk.Label(
            self.frame_status,
            text="💡 Pronto para usar. Selecione um usuário para editar ou excluir."
        )
        self.label_status.grid(row=0, column=0, sticky="w")
        
        # Label contador de usuários
        self.label_contador = ttk.Label(
            self.frame_status,
            text="Usuários: 0"
        )
        self.label_contador.grid(row=0, column=1, sticky="e")
        
        # Configura redimensionamento
        self.frame_status.columnconfigure(0, weight=1)
    
    def atualizar_status(self, mensagem: str):
        """
        Atualiza a mensagem da barra de status.
        
        Args:
            mensagem: Nova mensagem a ser exibida
        """
        self.label_status.config(text=mensagem)
        self.root.update_idletasks()
    
    def atualizar_contador_usuarios(self):
        """
        Atualiza o contador de usuários na barra de status.
        """
        try:
            total = contar_usuarios()
            self.label_contador.config(text=f"Usuários: {total}")
        except Exception as e:
            print(f"❌ Erro ao contar usuários: {e}")
    
    def limpar_formulario(self):
        """
        Limpa todos os campos do formulário.
        """
        self.var_nome.set("")
        self.var_email.set("")
        self.var_senha.set("")
        self.var_perfil.set("operador")
        self.usuario_selecionado_id = None
        
        # Desabilita botões de edição
        self.btn_atualizar.config(state="disabled")
        self.btn_excluir.config(state="disabled")
        
        self.atualizar_status("🧹 Formulário limpo. Digite os dados para adicionar novo usuário.")
    
    def validar_formulario(self) -> bool:
        """
        Valida os dados do formulário.
        
        Returns:
            bool: True se dados são válidos, False caso contrário
        """
        nome = self.var_nome.get().strip()
        email = self.var_email.get().strip()
        senha = self.var_senha.get().strip()
        perfil = self.var_perfil.get().strip()
        
        if not nome:
            messagebox.showerror("Erro", "Nome é obrigatório!")
            self.entry_nome.focus()
            return False
        
        if not email:
            messagebox.showerror("Erro", "Email é obrigatório!")
            self.entry_email.focus()
            return False
        
        if "@" not in email:
            messagebox.showerror("Erro", "Email deve ter formato válido!")
            self.entry_email.focus()
            return False
        
        if not senha:
            messagebox.showerror("Erro", "Senha é obrigatória!")
            self.entry_senha.focus()
            return False
        
        if len(senha) < 4:
            messagebox.showerror("Erro", "Senha deve ter pelo menos 4 caracteres!")
            self.entry_senha.focus()
            return False
        
        if perfil not in ["admin", "operador"]:
            messagebox.showerror("Erro", "Selecione um perfil válido!")
            return False
        
        return True
    
    def adicionar_usuario(self):
        """
        Adiciona um novo usuário usando os dados do formulário.
        """
        if not self.validar_formulario():
            return
        
        try:
            self.atualizar_status("⏳ Adicionando usuário...")
            
            nome = self.var_nome.get().strip()
            email = self.var_email.get().strip()
            senha = self.var_senha.get().strip()
            perfil = self.var_perfil.get().strip()
            
            sucesso = criar_usuario(nome, email, senha, perfil)
            
            if sucesso:
                messagebox.showinfo("Sucesso", f"Usuário '{nome}' criado com sucesso!")
                self.limpar_formulario()
                self.atualizar_lista_usuarios()
                self.atualizar_status("✅ Usuário adicionado com sucesso!")
            else:
                messagebox.showerror("Erro", "Falha ao criar usuário. Verifique se o email já não está em uso.")
                self.atualizar_status("❌ Erro ao adicionar usuário.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
            self.atualizar_status("❌ Erro inesperado ao adicionar usuário.")
            print(f"❌ Erro ao adicionar usuário: {e}")
    
    def atualizar_lista_usuarios(self):
        """
        Atualiza a lista de usuários exibida no Treeview.
        """
        try:
            self.atualizar_status("⏳ Carregando usuários...")
            
            # Limpa itens existentes
            for item in self.tree_usuarios.get_children():
                self.tree_usuarios.delete(item)
            
            # Carrega usuários
            usuarios = listar_usuarios()
            
            # Adiciona usuários ao Treeview
            for usuario in usuarios:
                # Formata data para exibição (apenas data, sem horário)
                data_cadastro = usuario['data_criacao']
                if ' ' in data_cadastro:
                    data_cadastro = data_cadastro.split(' ')[0]
                
                self.tree_usuarios.insert(
                    "",
                    "end",
                    values=(
                        usuario['id'],
                        usuario['nome'],
                        usuario['email'],
                        usuario['perfil'].title(),  # Primeira letra maiúscula
                        data_cadastro
                    )
                )
            
            # Atualiza contador
            self.atualizar_contador_usuarios()
            
            self.atualizar_status(f"✅ Lista atualizada. {len(usuarios)} usuário(s) encontrado(s).")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar usuários: {str(e)}")
            self.atualizar_status("❌ Erro ao carregar lista de usuários.")
            print(f"❌ Erro ao atualizar lista: {e}")
    
    def on_usuario_selecionado(self, event):
        """
        Evento disparado quando um usuário é selecionado na lista.
        
        Args:
            event: Evento do Tkinter
        """
        selecao = self.tree_usuarios.selection()
        
        if not selecao:
            # Nenhum item selecionado
            self.usuario_selecionado_id = None
            self.btn_atualizar.config(state="disabled")
            self.btn_excluir.config(state="disabled")
            return
        
        # Pega o primeiro item selecionado
        item = selecao[0]
        valores = self.tree_usuarios.item(item, "values")
        
        if valores:
            # Extrai dados do usuário selecionado
            self.usuario_selecionado_id = int(valores[0])
            nome = valores[1]
            email = valores[2]
            perfil = valores[3].lower()  # Converte de volta para minúscula
            
            # Preenche formulário com dados do usuário selecionado
            self.var_nome.set(nome)
            self.var_email.set(email)
            self.var_senha.set("")  # Não exibe senha por segurança
            self.var_perfil.set(perfil)
            
            # Habilita botões de edição
            self.btn_atualizar.config(state="normal")
            self.btn_excluir.config(state="normal")
            
            self.atualizar_status(f"👤 Usuário selecionado: {nome} - Você pode editar ou excluir.")
    
    def atualizar_usuario_selecionado(self):
        """
        Atualiza os dados do usuário selecionado.
        """
        if not self.usuario_selecionado_id:
            messagebox.showwarning("Aviso", "Selecione um usuário para atualizar!")
            return
        
        if not self.validar_formulario():
            return
        
        try:
            self.atualizar_status("⏳ Atualizando usuário...")
            
            nome = self.var_nome.get().strip()
            email = self.var_email.get().strip()
            senha = self.var_senha.get().strip()
            perfil = self.var_perfil.get().strip()
            
            # Se senha estiver vazia, não atualiza a senha
            senha_param = senha if senha else None
            
            sucesso = atualizar_usuario(
                self.usuario_selecionado_id,
                nome=nome,
                email=email,
                senha=senha_param,
                perfil=perfil
            )
            
            if sucesso:
                messagebox.showinfo("Sucesso", f"Usuário '{nome}' atualizado com sucesso!")
                self.limpar_formulario()
                self.atualizar_lista_usuarios()
                self.atualizar_status("✅ Usuário atualizado com sucesso!")
            else:
                messagebox.showerror("Erro", "Falha ao atualizar usuário.")
                self.atualizar_status("❌ Erro ao atualizar usuário.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
            self.atualizar_status("❌ Erro inesperado ao atualizar usuário.")
            print(f"❌ Erro ao atualizar usuário: {e}")
    
    def excluir_usuario_selecionado(self):
        """
        Exclui o usuário selecionado após confirmação.
        """
        if not self.usuario_selecionado_id:
            messagebox.showwarning("Aviso", "Selecione um usuário para excluir!")
            return
        
        nome = self.var_nome.get().strip()
        
        # Confirma exclusão
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o usuário '{nome}'?\n\n"
            f"⚠️ Esta ação não pode ser desfeita!",
            icon="warning"
        )
        
        if not resposta:
            return
        
        try:
            self.atualizar_status("⏳ Excluindo usuário...")
            
            sucesso = deletar_usuario(self.usuario_selecionado_id)
            
            if sucesso:
                messagebox.showinfo("Sucesso", f"Usuário '{nome}' excluído com sucesso!")
                self.limpar_formulario()
                self.atualizar_lista_usuarios()
                self.atualizar_status("✅ Usuário excluído com sucesso!")
            else:
                messagebox.showerror("Erro", "Falha ao excluir usuário.")
                self.atualizar_status("❌ Erro ao excluir usuário.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
            self.atualizar_status("❌ Erro inesperado ao excluir usuário.")
            print(f"❌ Erro ao excluir usuário: {e}")


def main():
    """
    Função principal que cria e executa a interface gráfica.
    """
    print("🚀 Iniciando interface de usuários...")
    
    try:
        # Cria janela principal
        root = tk.Tk()
        
        # Cria interface
        app = UsuariosUI(root)
        
        print("✅ Interface criada com sucesso!")
        print("💡 Feche a janela para encerrar a aplicação.")
        
        # Inicia loop principal do Tkinter
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erro ao iniciar interface: {e}")
        messagebox.showerror("Erro Fatal", f"Erro ao iniciar aplicação:\n{str(e)}")


if __name__ == "__main__":
    """
    Executa a interface quando o arquivo é chamado diretamente.
    
    Uso: python ui/usuarios_ui.py
    """
    main()