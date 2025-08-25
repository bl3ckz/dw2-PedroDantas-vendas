# 🚀 Como Executar o Projeto TechStore

Este guia explica como executar o projeto de e-commerce localmente para apresentação e avaliação.

## 📋 Pré-requisitos

Certifique-se de ter instalado:
- **Python 3.11 ou superior**
- **Node.js 20 ou superior**
- **npm** ou **pnpm** (recomendado)

## 🔧 Passo a Passo

### 1. Preparar o Backend (Flask)

```bash
# Navegar para o diretório do backend
cd ecommerce_project/backend/ecommerce_api

# Criar ambiente virtual Python (se não existir)
python -m venv venv

# Ativar o ambiente virtual
# No Linux/Mac:
source venv/bin/activate
# No Windows:
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar o servidor backend
python src/main.py
```

O backend estará rodando em: **http://localhost:5000**

### 2. Preparar o Frontend (React)

**Em um novo terminal:**

```bash
# Navegar para o diretório do frontend
cd ecommerce_project/frontend/ecommerce_frontend

# Instalar dependências
pnpm install
# ou se preferir npm:
# npm install

# Executar o servidor frontend
pnpm run dev
# ou com npm:
# npm run dev
```

O frontend estará rodando em: **http://localhost:5173**

### 3. Acessar a Aplicação

1. Abra seu navegador
2. Acesse: **http://localhost:5173**
3. O site estará funcionando completamente!

## 🧪 Como Testar as Funcionalidades

### Teste 1: Navegação
- ✅ Acesse a página inicial
- ✅ Clique em "Produtos" para ver o catálogo
- ✅ Navegue entre as páginas

### Teste 2: Cadastro de Usuário
- ✅ Clique em "Cadastrar"
- ✅ Preencha: Nome, Email, Senha
- ✅ Clique em "Criar Conta"
- ✅ Deve redirecionar para a home logado

### Teste 3: Login
- ✅ Clique em "Entrar"
- ✅ Use as credenciais criadas
- ✅ Deve fazer login com sucesso

### Teste 4: Carrinho de Compras
- ✅ Navegue até "Produtos"
- ✅ Clique em "Adicionar ao Carrinho"
- ✅ Veja o número no ícone do carrinho
- ✅ Clique no carrinho para ver os itens

### Teste 5: Finalização de Pedido
- ✅ No carrinho, clique "Finalizar Pedido"
- ✅ O pedido deve ser processado
- ✅ O carrinho deve ser limpo

## 📱 Teste de Responsividade

- ✅ Redimensione a janela do navegador
- ✅ Teste em dispositivos móveis
- ✅ Verifique se o layout se adapta

## 🗄️ Dados de Exemplo

O sistema já vem com produtos pré-cadastrados:
- Smartphone Samsung Galaxy - R$ 899,99
- Notebook Dell Inspiron - R$ 2.499,99
- Fone de Ouvido Bluetooth - R$ 299,99
- Smart TV 55 polegadas - R$ 1.899,99
- Mouse Gamer RGB - R$ 149,99
- Teclado Mecânico - R$ 299,99

## 🔧 Solução de Problemas

### Backend não inicia
```bash
# Verifique se o ambiente virtual está ativo
source venv/bin/activate

# Reinstale as dependências
pip install -r requirements.txt
```

### Frontend não carrega produtos
- Certifique-se que o backend está rodando na porta 5000
- Verifique se não há erros no console do navegador

### Erro de CORS
- O projeto já está configurado para CORS
- Certifique-se que ambos servidores estão rodando

### Banco de dados
- O SQLite é criado automaticamente
- Localizado em: `backend/ecommerce_api/src/database/app.db`
- Para resetar: delete o arquivo e reinicie o backend

## 📊 Portas Utilizadas

- **Backend (Flask)**: http://localhost:5000
- **Frontend (React)**: http://localhost:5173

## 🎯 Para Apresentação

1. **Inicie ambos os servidores** (backend e frontend)
2. **Acesse http://localhost:5173**
3. **Demonstre as funcionalidades** seguindo os testes acima
4. **Mostre o código** nos diretórios organizados
5. **Explique a arquitetura** usando o README.md

## 📁 Estrutura para Entrega

```
ecommerce_project/
├── README.md                 # Documentação completa
├── COMO_EXECUTAR.md         # Este arquivo
├── backend/                 # Código do servidor
└── frontend/                # Código da interface
```

## ✅ Checklist de Entrega

- [x] Backend Flask funcionando
- [x] Frontend React responsivo
- [x] Banco de dados SQLite
- [x] Sistema de autenticação
- [x] Carrinho de compras
- [x] Finalização de pedidos
- [x] Design moderno e responsivo
- [x] Código bem documentado
- [x] README completo
- [x] Instruções de execução

---

**Projeto pronto para apresentação e avaliação! 🎉**

