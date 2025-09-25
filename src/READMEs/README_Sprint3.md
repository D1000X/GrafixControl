# 🏁 Sprint 3 - Cadastro de Usuários

## 📋 Descrição

A Sprint 3 implementa o **módulo completo de usuários** para o sistema da gráfica, incluindo:
- ✅ Tabela de usuários atualizada com hash de senhas
- ✅ Módulo de lógica com operações CRUD completas  
- ✅ Interface gráfica Tkinter funcional
- ✅ Sistema de autenticação com hash SHA256
- ✅ Validações e tratamento de erros

## 🏗️ Estrutura de Arquivos Criados

```
projeto/
├─ database/
│  ├─ db.sqlite              # Banco atualizado (Sprint 2 + 3)
│  ├─ setup.py               # ✏️ Atualizado com nova tabela usuarios
│  └─ connection.py          # (Sprint 2 - não alterado)
├─ modules/
│  └─ usuarios.py            # 🆕 Módulo de lógica CRUD
├─ ui/
│  └─ usuarios_ui.py         # 🆕 Interface gráfica Tkinter
├─ exemplo_uso.py            # 🆕 Demonstração completa
└─ README_Sprint3.md         # 🆕 Esta documentação
```

## 🚀 Instalação e Primeiro Uso

### 1. **Setup Inicial do Banco**
```bash
# Cria/atualiza o banco com a nova tabela usuarios
python database/setup.py
```

### 2. **Testar Módulo de Usuários**
```bash
# Executa testes do módulo CRUD
python modules/usuarios.py
```

### 3. **Abrir Interface Gráfica**
```bash
# Abre a janela de gerenciamento de usuários
python ui/usuarios_ui.py
```

### 4. **Executar Exemplo Completo**
```bash
# Demonstração completa do sistema
python exemplo_uso.py
```

## 🗄️ Estrutura da Tabela `usuarios`

```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,                    -- Hash SHA256
    perfil TEXT NOT NULL,                   -- 'admin' ou 'operador'
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 🔐 Segurança de Senhas
- Senhas são armazenadas como **hash SHA256**
- Nunca armazenamos senhas em texto puro
- Função `gerar_hash_senha()` converte automaticamente

## 📚 Módulo `modules/usuarios.py`

### Funções Principais

| Função | Descrição | Exemplo |
|--------|-----------|---------|
| `criar_usuario()` | Cria novo usuário | `criar_usuario("João", "joao@email.com", "senha123", "operador")` |
| `listar_usuarios()` | Lista todos os usuários | `usuarios = listar_usuarios()` |
| `buscar_usuario_por_email()` | Busca por email | `usuario = buscar_usuario_por_email("joao@email.com")` |
| `buscar_usuario_por_id()` | Busca por ID | `usuario = buscar_usuario_por_id(1)` |
| `atualizar_usuario()` | Atualiza dados | `atualizar_usuario(1, nome="Novo Nome")` |
| `deletar_usuario()` | Remove usuário | `deletar_usuario(1)` |
| `verificar_login()` | Autentica usuário | `usuario = verificar_login("email", "senha")` |

### Exemplo de Uso do Módulo

```python
from modules.usuarios import criar_usuario, listar_usuarios, verificar_login

# Criar usuário
sucesso = criar_usuario(
    nome="Maria Silva",
    email="maria@grafica.com", 
    senha="senha123",
    perfil="admin"
)

# Listar usuários
usuarios = listar_usuarios()
for usuario in usuarios:
    print(f"{usuario['nome']} - {usuario['perfil']}")

# Verificar login
usuario_logado = verificar_login("maria@grafica.com", "senha123")
if usuario_logado:
    print(f"Login válido: {usuario_logado['nome']}")
```

## 🖥️ Interface Gráfica `ui/usuarios_ui.py`

### Funcionalidades da Interface

- **📝 Formulário de Cadastro**: Campos para nome, email, senha e perfil
- **📋 Lista de Usuários**: Visualização em tabela (Treeview)
- **🔄 Operações CRUD**: Botões para adicionar, atualizar, excluir
- **🔍 Seleção Intuitiva**: Clique no usuário para editar
- **✅ Validações**: Campos obrigatórios e formatos válidos
- **📊 Barra de Status**: Feedback em tempo real

### Layout da Interface

```
┌─────────────────────────────────────────────────────────────┐
│  🎨 Sistema Gráfica - Gerenciamento de Usuários            │
├─────────────────────────────────────────────────────────────┤
│  📝 Dados do Usuário                                        │
│  Nome: [____________]  Email: [____________]                │  
│  Senha: [___________]  Perfil: [Operador ▼]                │
├─────────────────────────────────────────────────────────────┤
│  👥 Usuários Cadastrados                                    │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ ID │ Nome        │ Email           │ Perfil │ Data     │ │
│  │ 1  │ Admin       │ admin@...       │ Admin  │ 22/09/25 │ │
│  │ 2  │ João Silva  │ joao@...        │ Operador│22/09/25 │ │
│  └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  [➕ Adicionar] [✏️ Atualizar] [🗑️ Excluir] [🧹 Limpar]  │
├─────────────────────────────────────────────────────────────┤
│  💡 Status: Pronto                    Usuários: 2          │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Como Usar a Interface

1. **➕ Adicionar Usuário**:
   - Preencha todos os campos
   - Clique em "Adicionar"
   - Usuario será criado e listado

2. **✏️ Editar Usuário**:
   - Clique no usuário na lista
   - Dados aparecerão no formulário
   - Modifique os campos desejados
   - Clique em "Atualizar"

3. **🗑️ Excluir Usuário**:
   - Selecione usuário na lista
   - Clique em "Excluir"
   - Confirme a exclusão

4. **🧹 Limpar Formulário**:
   - Clique em "Limpar" para resetar campos

## ⚡ Funcionalidades Avançadas

### 🔐 Autenticação
```python
from modules.usuarios import verificar_login

# Função de login
usuario = verificar_login("admin@grafica.com", "admin123")
if usuario:
    print(f"Bem-vindo, {usuario['nome']}!")
    print(f"Seu perfil: {usuario['perfil']}")
else:
    print("Credenciais inválidas!")
```

### 📊 Relatórios
```python
from modules.usuarios import contar_usuarios, listar_usuarios_por_perfil

# Estatísticas
total = contar_usuarios()
admins = listar_usuarios_por_perfil("admin")
operadores = listar_usuarios_por_perfil("operador")

print(f"Total: {total}")
print(f"Admins: {len(admins)}")
print(f"Operadores: {len(operadores)}")
```

## 🛡️ Segurança Implementada

- **🔐 Hash de Senhas**: SHA256 para todas as senhas
- **🛑 SQL Injection**: Parâmetros seguros em todas as queries
- **✅ Validações**: Email único, campos obrigatórios
- **🔒 Ocultação**: Senhas nunca exibidas em logs ou interface
- **🚫 Prevenção**: Emails duplicados bloqueados

## 📋 Validações Implementadas

### Validações do Módulo
- ✅ Nome obrigatório e não vazio
- ✅ Email obrigatório e com formato válido (@)
- ✅ Senha mínimo 4 caracteres
- ✅ Perfil apenas 'admin' ou 'operador'
- ✅ Email único no sistema

### Validações da Interface
- ✅ Todos os campos obrigatórios
- ✅ Feedback visual de erros
- ✅ Confirmação para exclusões
- ✅ Mensagens de status em tempo real

## 🐛 Tratamento de Erros

### Tipos de Erro Tratados
- **🔌 Conexão**: Problemas de banco de dados
- **📝 Validação**: Dados inválidos ou obrigatórios
- **🔄 Duplicação**: Email já existente
- **🗑️ Referência**: Usuário não encontrado
- **🖥️ Interface**: Erros de Tkinter

### Logs do Sistema
```
✅ Operações bem-sucedidas - Verde com emoji
❌ Erros e problemas - Vermelho com descrição  
ℹ️ Informações gerais - Azul neutro
⏳ Processamento - Amarelo temporário
🔐 Segurança - Roxo para operações sensíveis
```

## 📊 Dados de Teste Inclusos

O sistema cria automaticamente:
- **Admin Padrão**: 
  - Email: `admin@grafica.com`
  - Senha: `admin123`
  - Perfil: `admin`

Para criar mais usuários de teste, execute `exemplo_uso.py`.

## 🔄 Integração com Sprint 2

A Sprint 3 **estende** a Sprint 2:
- ✅ Usa `database/connection.py` (sem modificações)
- ✅ Atualiza `database/setup.py` (nova tabela usuarios)
- ✅ Mantém compatibilidade total
- ✅ Adiciona novos módulos sem quebrar existentes

## 🚀 Próximos Passos (Sprint 4+)

- **🔐 Sistema de Login**: Tela de autenticação
- **👥 Controle de Sessão**: Usuário logado ativo  
- **🎛️ Dashboard**: Interface principal do sistema
- **📊 Relatórios**: Módulo de relatórios avançados
- **🔒 Permissões**: Controle por perfil de usuário
- **📤 Backup**: Sistema de backup automático

## ❓ Problemas Comuns

### "Módulo não encontrado"
```bash
# Certifique-se de estar no diretório correto
cd projeto/
python ui/usuarios_ui.py
```

### "Banco não existe"  
```bash
# Execute o setup primeiro
python database/setup.py
```

### "Erro de permissão"
```bash
# Verifique permissões da pasta
chmod 755 database/
```

### Interface não abre
```bash
# Verifique se Tkinter está instalado
python -m tkinter
```

## 💡 Dicas de Uso

1. **Primeira execução**: Sempre rode `setup.py` primeiro
2. **Desenvolvimento**: Use `modules/usuarios.py` para testes
3. **Produção**: Use `ui/usuarios_ui.py` para operação normal
4. **Debug**: Verifique logs no console para erros
5. **Backup**: Copie `database/db.sqlite` regularmente

## 🎯 Objetivos Alcançados

- ✅ **Banco de Dados**: Tabela usuarios com hash de senhas
- ✅ **Módulo CRUD**: Operações completas e seguras
- ✅ **Interface Gráfica**: Tkinter funcional e intuitiva  
- ✅ **Validações**: Campos obrigatórios e formatos
- ✅ **Segurança**: Hash SHA256 e SQL injection protection
- ✅ **Documentação**: Código comentado e README detalhado
- ✅ **Testes**: Exemplos e validações automáticas
- ✅ **Integração**: Compatível com Sprint 2

---

🎉 **Sprint 3 - Cadastro de Usuários CONCLUÍDA COM SUCESSO!**

Sistema pronto para integração com as próximas funcionalidades da gráfica.