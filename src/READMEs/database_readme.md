# Sistema Gráfica - Sprint 2: Banco de Dados e Conexão

## 📋 Descrição

Este módulo implementa a Sprint 2 do sistema de gestão para gráfica, criando o banco de dados SQLite e o sistema de conexão reutilizável.

## 🏗️ Estrutura de Arquivos

```
projeto/
├─ database/
│  ├─ db.sqlite          # Banco de dados (gerado automaticamente)
│  ├─ setup.py           # Script de criação das tabelas
│  ├─ connection.py      # Módulo de conexão reutilizável
│  └─ README.md          # Este arquivo
```

## 🚀 Como Usar

### 1. Executar o Setup Inicial

Para criar o banco de dados e todas as tabelas:

```bash
python database/setup.py
```

Este comando irá:
- ✅ Criar o arquivo `db.sqlite` 
- ✅ Criar todas as 6 tabelas necessárias
- ✅ Inserir dados de teste
- ✅ Executar testes de validação
- ✅ Exibir relatório completo no console

### 2. Usar o Módulo de Conexão

```python
from database.connection import execute_query, get_connection, close_connection

# Exemplo de inserção
execute_query(
    "INSERT INTO clientes (nome, email) VALUES (?, ?)", 
    ("João Silva", "joao@email.com")
)

# Exemplo de consulta
clientes = execute_query("SELECT * FROM clientes")
for cliente in clientes:
    print(f"Cliente: {cliente['nome']}")

# Exemplo de conexão manual
conn = get_connection()
# ... operações customizadas ...
close_connection(conn)
```

## 🗄️ Estrutura das Tabelas

### 1. **usuarios**
- `id` - Chave primária
- `nome` - Nome do usuário
- `email` - Email único
- `senha` - Senha (será expandida na Sprint 3)
- `tipo` - Tipo de usuário (administrador, operador)
- `ativo` - Status ativo/inativo
- `data_criacao`, `data_atualizacao` - Timestamps

### 2. **clientes**
- `id` - Chave primária
- `nome` - Nome do cliente
- `empresa` - Nome da empresa
- `email`, `telefone` - Contatos
- `endereco`, `cidade`, `estado`, `cep` - Endereço completo
- `cpf_cnpj` - Documento único
- `observacoes` - Observações gerais
- `ativo` - Status ativo/inativo
- `data_cadastro`, `data_atualizacao` - Timestamps

### 3. **materiais**
- `id` - Chave primária
- `nome`, `descricao` - Identificação do material
- `categoria` - Categoria (papel, tinta, etc.)
- `unidade` - Unidade de medida
- `preco_unitario` - Preço por unidade
- `estoque_atual`, `estoque_minimo` - Controle de estoque
- `fornecedor` - Fornecedor principal
- `codigo_barras` - Código de barras
- `ativo` - Status ativo/inativo
- `data_cadastro`, `data_atualizacao` - Timestamps

### 4. **orcamentos**
- `id` - Chave primária
- `numero_orcamento` - Número único do orçamento
- `cliente_id` - FK para clientes
- `descricao_servico` - Descrição do trabalho
- `quantidade`, `valor_unitario`, `valor_total` - Valores
- `prazo_entrega` - Data de entrega
- `status` - Status do orçamento (pendente, aprovado, rejeitado)
- `observacoes` - Observações
- `data_criacao`, `data_aprovacao`, `data_vencimento` - Timestamps
- `usuario_id` - FK para usuários

### 5. **pagamentos**
- `id` - Chave primária
- `orcamento_id` - FK para orçamentos
- `valor_pagamento` - Valor pago
- `forma_pagamento` - Forma de pagamento
- `status_pagamento` - Status (pendente, pago, vencido)
- `data_vencimento`, `data_pagamento` - Datas
- `numero_comprovante` - Comprovante
- `observacoes` - Observações
- `data_criacao` - Timestamp
- `usuario_id` - FK para usuários

### 6. **producao**
- `id` - Chave primária
- `orcamento_id` - FK para orçamentos
- `status_producao` - Status da produção
- `data_inicio`, `data_previsao_fim`, `data_conclusao` - Cronograma
- `responsavel` - Responsável pela produção
- `equipamento_usado` - Equipamento utilizado
- `observacoes_producao` - Observações da produção
- `qualidade_aprovada` - Controle de qualidade
- `data_criacao`, `data_atualizacao` - Timestamps
- `usuario_id` - FK para usuários

## 🔧 Funcionalidades do Módulo de Conexão

### Funções Principais

- **`get_connection()`** - Estabelece conexão com SQLite
- **`close_connection(conn)`** - Fecha conexão
- **`execute_query(query, params=None)`** - Executa consultas SQL
- **`execute_many(query, params_list)`** - Execução em lote
- **`test_connection()`** - Testa conectividade

### Recursos Implementados

- ✅ Tratamento de exceções
- ✅ Logs informativos com emojis
- ✅ Suporte a parâmetros seguros (SQL injection protection)
- ✅ Row factory para acesso por nome de coluna
- ✅ Gerenciamento automático de conexões
- ✅ Contagem de linhas afetadas

## 📊 Dados de Teste Inclusos

O setup cria automaticamente:
- 1 usuário administrador (admin@grafica.com)
- 1 cliente exemplo (João Silva - Empresa ABC)
- 1 material exemplo (Papel A4 75g)

## ⚡ Requisitos

- Python 3.6+
- Módulo `sqlite3` (incluso no Python)
- Sistema operacional: Windows, Linux ou macOS

## 🔒 Segurança

- Uso de parâmetros seguros em todas as consultas
- Proteção contra SQL injection
- Validação de conexões antes das operações

## 🐛 Tratamento de Erros

- Exceções capturadas e logadas
- Mensagens de erro claras e informativas
- Conexões sempre fechadas adequadamente
- Rollback automático em caso de erro

## 📝 Logs do Sistema

O sistema exibe logs coloridos com emojis:
- ✅ Operações bem-sucedidas
- ❌ Erros e problemas  
- 🔧 Testes e validações
- 📋 Criação de tabelas
- 📊 Relatórios de dados

## 🚀 Próximos Passos (Sprint 3)

- Implementar autenticação de usuários
- Criar interface gráfica
- Adicionar validações de dados
- Implementar backup automático
- Criar relatórios avançados
